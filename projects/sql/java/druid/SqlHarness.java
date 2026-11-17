import java.math.BigDecimal;
import java.nio.ByteBuffer;
import java.nio.charset.CharacterCodingException;
import java.nio.charset.CodingErrorAction;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.TreeSet;
import com.alibaba.druid.DbType;
import com.alibaba.druid.sql.SQLUtils;
import com.alibaba.druid.sql.ast.SQLStatement;
import com.alibaba.druid.sql.ast.expr.SQLAggregateExpr;
import com.alibaba.druid.sql.ast.expr.SQLCharExpr;
import com.alibaba.druid.sql.ast.expr.SQLIntegerExpr;
import com.alibaba.druid.sql.ast.expr.SQLMethodInvokeExpr;
import com.alibaba.druid.sql.ast.expr.SQLNumberExpr;
import com.alibaba.druid.sql.ast.statement.SQLExprTableSource;
import com.alibaba.druid.sql.ast.statement.SQLInsertStatement;
import com.alibaba.druid.sql.ast.statement.SQLJoinTableSource;
import com.alibaba.druid.sql.ast.statement.SQLSelectQueryBlock;
import com.alibaba.druid.sql.ast.statement.SQLSelectStatement;
import com.alibaba.druid.sql.ast.statement.SQLTableSource;
import com.alibaba.druid.sql.visitor.SQLASTVisitorAdapter;

/**
 * Druid SQL parser: SQLUtils.parseStatements(local SQL text, DbType.mysql).
 * Every summary field is read from Druid's AST (statements, query blocks, visitor callbacks).
 */
public final class SqlHarness {
    private static final class Collector extends SQLASTVisitorAdapter {
        final TreeSet<String> tables = new TreeSet<>();
        final TreeSet<String> functions = new TreeSet<>();
        final List<String[]> literals = new ArrayList<>();

        @Override public boolean visit(SQLExprTableSource source) {
            tables.add(source.getTableName(true).toLowerCase());
            return true;
        }
        @Override public boolean visit(SQLAggregateExpr expr) {
            functions.add(expr.getMethodName().toLowerCase());
            return true;
        }
        @Override public boolean visit(SQLMethodInvokeExpr expr) {
            functions.add(expr.getMethodName().toLowerCase());
            return true;
        }
        @Override public boolean visit(SQLCharExpr expr) {
            literals.add(new String[]{"string", expr.getText()});
            return true;
        }
        @Override public boolean visit(SQLIntegerExpr expr) {
            literals.add(new String[]{"number", expr.getNumber().toString()});
            return true;
        }
        @Override public boolean visit(SQLNumberExpr expr) {
            Number number = expr.getNumber();
            literals.add(new String[]{"number", number instanceof BigDecimal decimal ? decimal.toPlainString() : number.toString()});
            return true;
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

    static int joins(SQLTableSource source) {
        if (source instanceof SQLJoinTableSource join) return 1 + joins(join.getLeft()) + joins(join.getRight());
        return 0;
    }

    static String summarize(SQLStatement statement) {
        Collector collector = new Collector();
        statement.accept(collector);
        if (statement instanceof SQLSelectStatement select
                && select.getSelect().getQuery() instanceof SQLSelectQueryBlock block) {
            int groupBy = block.getGroupBy() == null ? 0 : block.getGroupBy().getItems().size();
            int orderBy = block.getOrderBy() == null ? 0 : block.getOrderBy().getItems().size();
            return "{\"kind\":\"select\",\"tables\":" + names(collector.tables)
                    + ",\"select_items\":" + block.getSelectList().size()
                    + ",\"joins\":" + joins(block.getFrom())
                    + ",\"where\":" + (block.getWhere() != null)
                    + ",\"group_by\":" + groupBy + ",\"order_by\":" + orderBy
                    + ",\"functions\":" + names(collector.functions)
                    + ",\"literals\":" + collector.literalJson() + "}";
        }
        if (statement instanceof SQLInsertStatement insert) {
            return "{\"kind\":\"insert\",\"tables\":" + names(collector.tables)
                    + ",\"columns\":" + insert.getColumns().size()
                    + ",\"rows\":" + insert.getValuesList().size()
                    + ",\"literals\":" + collector.literalJson() + "}";
        }
        return "{\"kind\":" + quote(statement.getClass().getSimpleName().toLowerCase()) + "}";
    }

    static String parse(byte[] data) throws CharacterCodingException {
        if (data.length == 0 || data.length > (1 << 20)) throw new IllegalArgumentException("input outside harness limit");
        String text = StandardCharsets.UTF_8.newDecoder()
                .onMalformedInput(CodingErrorAction.REPORT)
                .onUnmappableCharacter(CodingErrorAction.REPORT)
                .decode(ByteBuffer.wrap(data)).toString();
        List<SQLStatement> statements = SQLUtils.parseStatements(text, DbType.mysql);
        List<String> summaries = new ArrayList<>();
        for (SQLStatement statement : statements) summaries.add(summarize(statement));
        return "{\"statement_count\":" + summaries.size() + ",\"statements\":[" + String.join(",", summaries) + "]}";
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (com.alibaba.druid.sql.parser.ParserException | IllegalArgumentException | CharacterCodingException rejected) { }
    }

    public static void main(String[] args) throws Exception {
        System.out.println(parse(Files.readAllBytes(Path.of(args[0]))));
    }
}
