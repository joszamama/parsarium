import java.nio.ByteBuffer;
import java.nio.charset.CharacterCodingException;
import java.nio.charset.CodingErrorAction;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.TreeSet;
import org.apache.spark.sql.catalyst.analysis.UnresolvedFunction;
import org.apache.spark.sql.catalyst.analysis.UnresolvedInlineTable;
import org.apache.spark.sql.catalyst.analysis.UnresolvedRelation;
import org.apache.spark.sql.catalyst.expressions.Expression;
import org.apache.spark.sql.catalyst.expressions.Literal;
import org.apache.spark.sql.catalyst.parser.CatalystSqlParser$;
import org.apache.spark.sql.catalyst.parser.ParseException;
import org.apache.spark.sql.catalyst.plans.logical.Aggregate;
import org.apache.spark.sql.catalyst.plans.logical.Filter;
import org.apache.spark.sql.catalyst.plans.logical.InsertIntoStatement;
import org.apache.spark.sql.catalyst.plans.logical.Join;
import org.apache.spark.sql.catalyst.plans.logical.LogicalPlan;
import org.apache.spark.sql.catalyst.plans.logical.Project;
import org.apache.spark.sql.catalyst.plans.logical.Sort;
import org.apache.spark.sql.types.NumericType;
import org.apache.spark.sql.types.StringType;
import scala.collection.JavaConverters;

/**
 * Spark SQL parser: CatalystSqlParser.parsePlan(local SQL text) -> unresolved LogicalPlan.
 * The plan is the parser's own syntax tree (AstBuilder output before analysis): Sort, Aggregate/Project,
 * Filter, Join, SubqueryAlias and UnresolvedRelation for the query; InsertIntoStatement over an
 * UnresolvedInlineTable for the insert. Every summary field is read from those nodes and their expressions;
 * literal kinds come from Literal.dataType and the parser-recorded origin span.
 */
public final class SqlHarness {
    private static final class Summary {
        final TreeSet<String> tables = new TreeSet<>();
        final TreeSet<String> functions = new TreeSet<>();
        final List<String[]> literals = new ArrayList<>();
        int selectItems = -1, joins = 0, groupBy = 0, orderBy = 0;
        boolean where = false;
        boolean select = false;

        void plan(LogicalPlan node) {
            if (node instanceof UnresolvedRelation relation) {
                tables.add(String.join(".", list(relation.multipartIdentifier())).toLowerCase(Locale.ROOT));
            } else if (node instanceof Join) {
                joins++;
            } else if (node instanceof Filter) {
                where = true;
            } else if (node instanceof Aggregate aggregate) {
                groupBy = aggregate.groupingExpressions().size();
                if (selectItems < 0) selectItems = aggregate.aggregateExpressions().size();
                select = true;
            } else if (node instanceof Project project) {
                if (selectItems < 0) selectItems = project.projectList().size();
                select = true;
            } else if (node instanceof Sort sort) {
                orderBy = sort.order().size();
            }
            for (Expression expression : list(node.expressions())) expression(expression);
            for (LogicalPlan child : list(node.children())) plan(child);
        }

        void expression(Expression node) {
            if (node instanceof UnresolvedFunction function) {
                functions.add(String.join(".", list(function.nameParts())).toLowerCase(Locale.ROOT));
            } else if (node instanceof Literal literal && literal.value() != null) {
                String token = sourceToken(literal);
                if (literal.dataType() instanceof StringType && (token.startsWith("'") || token.startsWith("\""))) {
                    literals.add(new String[]{"string", literal.value().toString()});
                } else if (literal.dataType() instanceof NumericType && token.equals(literal.value().toString())) {
                    literals.add(new String[]{"number", literal.value().toString()});
                }
            }
            for (Expression child : list(node.children())) expression(child);
        }

        String literalJson() {
            literals.sort((a, b) -> a[0].equals(b[0]) ? a[1].compareTo(b[1]) : a[0].compareTo(b[0]));
            List<String> pairs = new ArrayList<>();
            for (String[] literal : literals) pairs.add("[" + quote(literal[0]) + "," + quote(literal[1]) + "]");
            return "[" + String.join(",", pairs) + "]";
        }
    }

    /**
     * The source text of a literal's parser origin span. AstBuilder rewrites COUNT(*) to count(1); that
     * synthesized Literal carries the function call's span, so only literals whose span is the literal
     * token itself are reported.
     */
    static String sourceToken(Literal literal) {
        var origin = literal.origin();
        if (origin.sqlText().isEmpty() || origin.startIndex().isEmpty() || origin.stopIndex().isEmpty()) return "";
        String text = origin.sqlText().get();
        int start = (Integer) origin.startIndex().get();
        int stop = (Integer) origin.stopIndex().get();
        return start < 0 || stop >= text.length() || stop < start ? "" : text.substring(start, stop + 1);
    }

    static <T> List<T> list(scala.collection.Seq<T> seq) {
        return JavaConverters.seqAsJavaList(seq);
    }

    static String quote(String text) {
        StringBuilder out = new StringBuilder("\"");
        for (char c : text.toCharArray()) {
            if (c == '"' || c == '\\') out.append('\\').append(c);
            else if (c < 0x20) out.append(String.format("\\u%04x", (int) c));
            else out.append(c);
        }
        return out.append('"').toString();
    }

    static String names(TreeSet<String> values) {
        List<String> quoted = new ArrayList<>();
        for (String value : values) quoted.add(quote(value));
        return "[" + String.join(",", quoted) + "]";
    }

    static String summarize(LogicalPlan plan) {
        Summary summary = new Summary();
        if (plan instanceof InsertIntoStatement insert && insert.query() instanceof UnresolvedInlineTable values) {
            summary.plan(insert.table());
            summary.plan(values);
            return "{\"kind\":\"insert\",\"tables\":" + names(summary.tables)
                    + ",\"columns\":" + insert.userSpecifiedCols().size()
                    + ",\"rows\":" + values.rows().size()
                    + ",\"literals\":" + summary.literalJson() + "}";
        }
        summary.plan(plan);
        if (summary.select) {
            return "{\"kind\":\"select\",\"tables\":" + names(summary.tables)
                    + ",\"select_items\":" + summary.selectItems
                    + ",\"joins\":" + summary.joins
                    + ",\"where\":" + summary.where
                    + ",\"group_by\":" + summary.groupBy + ",\"order_by\":" + summary.orderBy
                    + ",\"functions\":" + names(summary.functions)
                    + ",\"literals\":" + summary.literalJson() + "}";
        }
        return "{\"kind\":" + quote(plan.nodeName().toLowerCase(Locale.ROOT)) + "}";
    }

    static String parse(byte[] data) throws CharacterCodingException {
        if (data.length == 0 || data.length > (1 << 20)) throw new IllegalArgumentException("input outside harness limit");
        String text = StandardCharsets.UTF_8.newDecoder()
                .onMalformedInput(CodingErrorAction.REPORT)
                .onUnmappableCharacter(CodingErrorAction.REPORT)
                .decode(ByteBuffer.wrap(data)).toString();
        LogicalPlan plan = CatalystSqlParser$.MODULE$.parsePlan(text);
        return "{\"statement_count\":1,\"statements\":[" + summarize(plan) + "]}";
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (Exception rejected) {
            // Scala declares no checked exceptions, so ParseException (a checked AnalysisException) is caught here.
            if (!(rejected instanceof ParseException || rejected instanceof IllegalArgumentException
                    || rejected instanceof CharacterCodingException)) {
                throw rejected instanceof RuntimeException runtime ? runtime : new RuntimeException(rejected);
            }
        }
    }

    public static void main(String[] args) throws Exception {
        System.out.println(parse(Files.readAllBytes(Path.of(args[0]))));
    }
}
