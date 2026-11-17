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
import io.trino.sql.parser.ParsingException;
import io.trino.sql.parser.SqlParser;
import io.trino.sql.tree.AliasedRelation;
import io.trino.sql.tree.DecimalLiteral;
import io.trino.sql.tree.DefaultTraversalVisitor;
import io.trino.sql.tree.FunctionCall;
import io.trino.sql.tree.GroupingElement;
import io.trino.sql.tree.Insert;
import io.trino.sql.tree.Join;
import io.trino.sql.tree.LongLiteral;
import io.trino.sql.tree.OrderBy;
import io.trino.sql.tree.Query;
import io.trino.sql.tree.QuerySpecification;
import io.trino.sql.tree.Relation;
import io.trino.sql.tree.SimpleGroupBy;
import io.trino.sql.tree.Statement;
import io.trino.sql.tree.StringLiteral;
import io.trino.sql.tree.Table;
import io.trino.sql.tree.Values;

/**
 * Trino SQL parser: SqlParser.createStatement(local SQL text without its terminating semicolon).
 * Trino's grammar parses one statement without a terminator (the Trino CLI strips it before submitting);
 * the adapter removes one trailing ';' and trailing whitespace and nothing else.
 * Every summary field is read from Trino's AST (Query, QuerySpecification, Insert, Values, visitor callbacks).
 */
public final class SqlHarness {
    private static final SqlParser PARSER = new SqlParser();

    private static final class Collector extends DefaultTraversalVisitor<Void> {
        final TreeSet<String> tables = new TreeSet<>();
        final TreeSet<String> functions = new TreeSet<>();
        final List<String[]> literals = new ArrayList<>();

        @Override protected Void visitTable(Table node, Void context) {
            tables.add(node.getName().toString().toLowerCase(Locale.ROOT));
            return super.visitTable(node, context);
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
            literals.add(new String[]{"number", node.getValue()});
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
                .decode(ByteBuffer.wrap(data)).toString().stripTrailing();
        if (text.endsWith(";")) text = text.substring(0, text.length() - 1);
        String summary = summarize(PARSER.createStatement(text));
        return "{\"statement_count\":1,\"statements\":[" + summary + "]}";
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (ParsingException | IllegalArgumentException | CharacterCodingException rejected) { }
    }

    public static void main(String[] args) throws Exception {
        System.out.println(parse(Files.readAllBytes(Path.of(args[0]))));
    }
}
