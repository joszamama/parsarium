import java.math.BigDecimal;
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
import org.apache.calcite.sql.SqlBasicCall;
import org.apache.calcite.sql.SqlCall;
import org.apache.calcite.sql.SqlCharStringLiteral;
import org.apache.calcite.sql.SqlFunction;
import org.apache.calcite.sql.SqlIdentifier;
import org.apache.calcite.sql.SqlInsert;
import org.apache.calcite.sql.SqlJoin;
import org.apache.calcite.sql.SqlKind;
import org.apache.calcite.sql.SqlLiteral;
import org.apache.calcite.sql.SqlNode;
import org.apache.calcite.sql.SqlNodeList;
import org.apache.calcite.sql.SqlNumericLiteral;
import org.apache.calcite.sql.SqlOrderBy;
import org.apache.calcite.sql.SqlSelect;
import org.apache.calcite.sql.parser.SqlParseException;
import org.apache.calcite.sql.parser.SqlParser;
import org.apache.calcite.sql.util.SqlBasicVisitor;

/**
 * Apache Calcite SQL parser: SqlParser.create(local SQL text, SqlParser.config()).parseStmtList().
 * Every summary field is read from Calcite's SqlNode tree (SqlOrderBy, SqlSelect, SqlJoin, SqlInsert, visitor callbacks).
 */
public final class SqlHarness {
    private static final class Collector extends SqlBasicVisitor<Void> {
        final TreeSet<String> functions = new TreeSet<>();
        final List<String[]> literals = new ArrayList<>();

        @Override public Void visit(SqlCall call) {
            if (call.getOperator() instanceof SqlFunction function) {
                functions.add(function.getName().toLowerCase(Locale.ROOT));
            }
            return super.visit(call);
        }
        @Override public Void visit(SqlLiteral literal) {
            if (literal instanceof SqlCharStringLiteral text) {
                literals.add(new String[]{"string", text.getValueAs(String.class)});
            } else if (literal instanceof SqlNumericLiteral number) {
                literals.add(new String[]{"number", number.getValueAs(BigDecimal.class).toPlainString()});
            }
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

    static String tableName(SqlIdentifier identifier) {
        return String.join(".", identifier.names).toLowerCase(Locale.ROOT);
    }

    /** Walks a FROM clause: joins, AS aliases and base-table identifiers. Returns the join count. */
    static int fromClause(SqlNode node, TreeSet<String> tables) {
        if (node instanceof SqlJoin join) {
            return 1 + fromClause(join.getLeft(), tables) + fromClause(join.getRight(), tables);
        }
        if (node instanceof SqlBasicCall call && call.getKind() == SqlKind.AS) {
            return fromClause(call.operand(0), tables);
        }
        if (node instanceof SqlIdentifier identifier) tables.add(tableName(identifier));
        return 0;
    }

    static int size(SqlNodeList list) {
        return list == null ? 0 : list.size();
    }

    static String summarize(SqlNode statement) {
        Collector collector = new Collector();
        statement.accept(collector);
        SqlNodeList orderList = null;
        SqlNode query = statement;
        if (query instanceof SqlOrderBy orderBy) {
            orderList = orderBy.orderList;
            query = orderBy.query;
        }
        if (query instanceof SqlSelect select) {
            if (orderList == null) orderList = select.getOrderList();
            TreeSet<String> tables = new TreeSet<>();
            int joins = select.getFrom() == null ? 0 : fromClause(select.getFrom(), tables);
            return "{\"kind\":\"select\",\"tables\":" + names(tables)
                    + ",\"select_items\":" + size(select.getSelectList())
                    + ",\"joins\":" + joins
                    + ",\"where\":" + (select.getWhere() != null)
                    + ",\"group_by\":" + size(select.getGroup())
                    + ",\"order_by\":" + size(orderList)
                    + ",\"functions\":" + names(collector.functions)
                    + ",\"literals\":" + collector.literalJson() + "}";
        }
        if (statement instanceof SqlInsert insert
                && insert.getSource() instanceof SqlBasicCall values && values.getKind() == SqlKind.VALUES) {
            TreeSet<String> tables = new TreeSet<>();
            fromClause(insert.getTargetTable(), tables);
            return "{\"kind\":\"insert\",\"tables\":" + names(tables)
                    + ",\"columns\":" + size(insert.getTargetColumnList())
                    + ",\"rows\":" + values.operandCount()
                    + ",\"literals\":" + collector.literalJson() + "}";
        }
        return "{\"kind\":" + quote(statement.getKind().lowerName) + "}";
    }

    static String parse(byte[] data) throws CharacterCodingException, SqlParseException {
        if (data.length == 0 || data.length > (1 << 20)) throw new IllegalArgumentException("input outside harness limit");
        String text = StandardCharsets.UTF_8.newDecoder()
                .onMalformedInput(CodingErrorAction.REPORT)
                .onUnmappableCharacter(CodingErrorAction.REPORT)
                .decode(ByteBuffer.wrap(data)).toString();
        SqlNodeList statements = SqlParser.create(text, SqlParser.config()).parseStmtList();
        List<String> summaries = new ArrayList<>();
        for (SqlNode statement : statements) summaries.add(summarize(statement));
        return "{\"statement_count\":" + summaries.size() + ",\"statements\":[" + String.join(",", summaries) + "]}";
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (SqlParseException | IllegalArgumentException | CharacterCodingException rejected) { }
    }

    public static void main(String[] args) throws Exception {
        System.out.println(parse(Files.readAllBytes(Path.of(args[0]))));
    }
}
