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
import net.sf.jsqlparser.JSQLParserException;
import net.sf.jsqlparser.expression.DoubleValue;
import net.sf.jsqlparser.expression.Function;
import net.sf.jsqlparser.expression.LongValue;
import net.sf.jsqlparser.expression.StringValue;
import net.sf.jsqlparser.expression.operators.relational.ExpressionList;
import net.sf.jsqlparser.expression.operators.relational.ParenthesedExpressionList;
import net.sf.jsqlparser.parser.CCJSqlParserUtil;
import net.sf.jsqlparser.statement.Statement;
import net.sf.jsqlparser.statement.insert.Insert;
import net.sf.jsqlparser.statement.select.PlainSelect;
import net.sf.jsqlparser.statement.select.Values;
import net.sf.jsqlparser.util.TablesNamesFinder;

/**
 * JSqlParser: CCJSqlParserUtil.parseStatements(local SQL text) with the default parser features.
 * Every summary field is read from JSqlParser's statement objects (PlainSelect, Insert) and a
 * TablesNamesFinder subclass that also records function names and literal values.
 */
public final class SqlHarness {
    private static final class Collector extends TablesNamesFinder<Void> {
        final TreeSet<String> functions = new TreeSet<>();
        final List<String[]> literals = new ArrayList<>();

        @Override public <S> Void visit(Function function, S context) {
            functions.add(function.getName().toLowerCase(Locale.ROOT));
            return super.visit(function, context);
        }
        @Override public <S> Void visit(StringValue value, S context) {
            literals.add(new String[]{"string", value.getValue()});
            return super.visit(value, context);
        }
        @Override public <S> Void visit(LongValue value, S context) {
            literals.add(new String[]{"number", value.getStringValue()});
            return super.visit(value, context);
        }
        @Override public <S> Void visit(DoubleValue value, S context) {
            literals.add(new String[]{"number", value.toString()});
            return super.visit(value, context);
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

    static String names(Iterable<String> values) {
        TreeSet<String> sorted = new TreeSet<>();
        for (String value : values) sorted.add(value.toLowerCase(Locale.ROOT));
        List<String> quoted = new ArrayList<>();
        for (String value : sorted) quoted.add(quote(value));
        return "[" + String.join(",", quoted) + "]";
    }

    static String summarize(Statement statement) {
        Collector collector = new Collector();
        String tables = names(collector.getTables(statement));
        if (statement instanceof PlainSelect select) {
            int groupBy = select.getGroupBy() == null ? 0 : select.getGroupBy().getGroupByExpressionList().size();
            int orderBy = select.getOrderByElements() == null ? 0 : select.getOrderByElements().size();
            return "{\"kind\":\"select\",\"tables\":" + tables
                    + ",\"select_items\":" + select.getSelectItems().size()
                    + ",\"joins\":" + (select.getJoins() == null ? 0 : select.getJoins().size())
                    + ",\"where\":" + (select.getWhere() != null)
                    + ",\"group_by\":" + groupBy + ",\"order_by\":" + orderBy
                    + ",\"functions\":" + names(collector.functions)
                    + ",\"literals\":" + collector.literalJson() + "}";
        }
        // Insert.getValues() casts the insert's query to Values; INSERT ... SELECT has no VALUES rows.
        if (statement instanceof Insert insert && insert.getSelect() instanceof Values values) {
            // VALUES (a, b) is one ParenthesedExpressionList holding the row's values; VALUES (a), (b)
            // is an ExpressionList with one ParenthesedExpressionList per row.
            ExpressionList<?> expressions = values.getExpressions();
            int rows = expressions instanceof ParenthesedExpressionList ? 1 : expressions.size();
            return "{\"kind\":\"insert\",\"tables\":" + tables
                    + ",\"columns\":" + (insert.getColumns() == null ? 0 : insert.getColumns().size())
                    + ",\"rows\":" + rows
                    + ",\"literals\":" + collector.literalJson() + "}";
        }
        return "{\"kind\":" + quote(statement.getClass().getSimpleName().toLowerCase(Locale.ROOT)) + "}";
    }

    static String parse(byte[] data) throws CharacterCodingException, JSQLParserException {
        if (data.length == 0 || data.length > (1 << 20)) throw new IllegalArgumentException("input outside harness limit");
        String text = StandardCharsets.UTF_8.newDecoder()
                .onMalformedInput(CodingErrorAction.REPORT)
                .onUnmappableCharacter(CodingErrorAction.REPORT)
                .decode(ByteBuffer.wrap(data)).toString();
        List<String> summaries = new ArrayList<>();
        for (Statement statement : CCJSqlParserUtil.parseStatements(text)) summaries.add(summarize(statement));
        return "{\"statement_count\":" + summaries.size() + ",\"statements\":[" + String.join(",", summaries) + "]}";
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (JSQLParserException | IllegalArgumentException | CharacterCodingException rejected) { }
    }

    public static void main(String[] args) throws Exception {
        System.out.println(parse(Files.readAllBytes(Path.of(args[0]))));
    }
}
