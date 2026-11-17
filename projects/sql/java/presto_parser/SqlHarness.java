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
import com.facebook.presto.sql.parser.ParsingException;
import com.facebook.presto.sql.parser.ParsingOptions;
import com.facebook.presto.sql.parser.SqlParser;
import com.facebook.presto.sql.parser.StatementSplitter;
import com.facebook.presto.sql.tree.AliasedRelation;
import com.facebook.presto.sql.tree.DecimalLiteral;
import com.facebook.presto.sql.tree.DefaultTraversalVisitor;
import com.facebook.presto.sql.tree.FunctionCall;
import com.facebook.presto.sql.tree.GroupingElement;
import com.facebook.presto.sql.tree.Insert;
import com.facebook.presto.sql.tree.Join;
import com.facebook.presto.sql.tree.LongLiteral;
import com.facebook.presto.sql.tree.OrderBy;
import com.facebook.presto.sql.tree.Query;
import com.facebook.presto.sql.tree.QuerySpecification;
import com.facebook.presto.sql.tree.Relation;
import com.facebook.presto.sql.tree.SimpleGroupBy;
import com.facebook.presto.sql.tree.Statement;
import com.facebook.presto.sql.tree.StringLiteral;
import com.facebook.presto.sql.tree.Table;
import com.facebook.presto.sql.tree.Values;

/**
 * Presto SQL parser: StatementSplitter over local SQL text, then
 * SqlParser.createStatement(statement, ParsingOptions with DecimalLiteralTreatment.AS_DECIMAL).
 * Every summary field is read from Presto's AST (Query, QuerySpecification, Insert, Values, visitor callbacks).
 */
public final class SqlHarness {
    private static final SqlParser PARSER = new SqlParser();
    private static final ParsingOptions OPTIONS = ParsingOptions.builder()
            .setDecimalLiteralTreatment(ParsingOptions.DecimalLiteralTreatment.AS_DECIMAL).build();

    private static final class Collector extends DefaultTraversalVisitor<Void, Void> {
        final TreeSet<String> tables = new TreeSet<>();
        final TreeSet<String> functions = new TreeSet<>();
        final List<String[]> literals = new ArrayList<>();

        @Override protected Void visitTable(Table node, Void context) {
            tables.add(node.getName().toString().toLowerCase(Locale.ROOT));
            return null;
        }
        @Override protected Void visitFunctionCall(FunctionCall node, Void context) {
            functions.add(node.getName().toString().toLowerCase(Locale.ROOT));
            return super.visitFunctionCall(node, context);
        }
        @Override protected Void visitStringLiteral(StringLiteral node, Void context) {
            literals.add(new String[]{"string", node.getValue()});
            return null;
        }
        @Override protected Void visitLongLiteral(LongLiteral node, Void context) {
            literals.add(new String[]{"number", Long.toString(node.getValue())});
            return null;
        }
        @Override protected Void visitDecimalLiteral(DecimalLiteral node, Void context) {
            literals.add(new String[]{"number", node.getValue()});
            return null;
        }

        String literalJson() {
            literals.sort((a, b) -> a[0].equals(b[0]) ? a[1].compareTo(b[1]) : a[0].compareTo(b[0]));
            List<String> pairs = new ArrayList<>();
            for (String[] literal : literals) pairs.add("[" + quote(literal[0]) + "," + quote(literal[1]) + "]");
            return "[" + String.join(",", pairs) + "]";
        }
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

    static int joins(Relation relation) {
        if (relation instanceof Join join) return 1 + joins(join.getLeft()) + joins(join.getRight());
        if (relation instanceof AliasedRelation aliased) return joins(aliased.getRelation());
        return 0;
    }

    static String summarize(Statement statement) {
        Collector collector = new Collector();
        collector.process(statement, null);
        if (statement instanceof Query query && query.getQueryBody() instanceof QuerySpecification spec) {
            int groupBy = 0;
            if (spec.getGroupBy().isPresent()) {
                for (GroupingElement element : spec.getGroupBy().get().getGroupingElements()) {
                    groupBy += element instanceof SimpleGroupBy simple ? simple.getExpressions().size() : 1;
                }
            }
            OrderBy orderBy = spec.getOrderBy().orElse(query.getOrderBy().orElse(null));
            return "{\"kind\":\"select\",\"tables\":" + names(collector.tables)
                    + ",\"select_items\":" + spec.getSelect().getSelectItems().size()
                    + ",\"joins\":" + spec.getFrom().map(SqlHarness::joins).orElse(0)
                    + ",\"where\":" + spec.getWhere().isPresent()
                    + ",\"group_by\":" + groupBy
                    + ",\"order_by\":" + (orderBy == null ? 0 : orderBy.getSortItems().size())
                    + ",\"functions\":" + names(collector.functions)
                    + ",\"literals\":" + collector.literalJson() + "}";
        }
        if (statement instanceof Insert insert && insert.getQuery().getQueryBody() instanceof Values values) {
            collector.tables.add(insert.getTarget().toString().toLowerCase(Locale.ROOT));
            return "{\"kind\":\"insert\",\"tables\":" + names(collector.tables)
                    + ",\"columns\":" + insert.getColumns().map(List::size).orElse(0)
                    + ",\"rows\":" + values.getRows().size()
                    + ",\"literals\":" + collector.literalJson() + "}";
        }
        return "{\"kind\":" + quote(statement.getClass().getSimpleName().toLowerCase(Locale.ROOT)) + "}";
    }

    static String parse(byte[] data) throws CharacterCodingException {
        if (data.length == 0 || data.length > (1 << 20)) throw new IllegalArgumentException("input outside harness limit");
        String text = StandardCharsets.UTF_8.newDecoder()
                .onMalformedInput(CodingErrorAction.REPORT)
                .onUnmappableCharacter(CodingErrorAction.REPORT)
                .decode(ByteBuffer.wrap(data)).toString();
        List<String> summaries = new ArrayList<>();
        for (StatementSplitter.Statement piece : new StatementSplitter(text).getCompleteStatements()) {
            summaries.add(summarize(PARSER.createStatement(piece.statement(), OPTIONS)));
        }
        return "{\"statement_count\":" + summaries.size() + ",\"statements\":[" + String.join(",", summaries) + "]}";
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (ParsingException | IllegalArgumentException | CharacterCodingException rejected) { }
    }

    public static void main(String[] args) throws Exception {
        System.out.println(parse(Files.readAllBytes(Path.of(args[0]))));
    }
}
