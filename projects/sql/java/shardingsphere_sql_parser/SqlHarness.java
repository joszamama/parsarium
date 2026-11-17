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
import java.util.Properties;
import java.util.TreeSet;
import org.apache.shardingsphere.sql.parser.api.CacheOption;
import org.apache.shardingsphere.sql.parser.api.SQLParserEngine;
import org.apache.shardingsphere.sql.parser.api.SQLVisitorEngine;
import org.apache.shardingsphere.sql.parser.core.ParseASTNode;
import org.apache.shardingsphere.sql.parser.exception.SQLParsingException;
import org.apache.shardingsphere.sql.parser.sql.common.segment.dml.assignment.InsertValuesSegment;
import org.apache.shardingsphere.sql.parser.sql.common.segment.dml.expr.BinaryOperationExpression;
import org.apache.shardingsphere.sql.parser.sql.common.segment.dml.expr.ExpressionSegment;
import org.apache.shardingsphere.sql.parser.sql.common.segment.dml.expr.FunctionSegment;
import org.apache.shardingsphere.sql.parser.sql.common.segment.dml.expr.simple.LiteralExpressionSegment;
import org.apache.shardingsphere.sql.parser.sql.common.segment.dml.item.AggregationProjectionSegment;
import org.apache.shardingsphere.sql.parser.sql.common.segment.dml.item.ExpressionProjectionSegment;
import org.apache.shardingsphere.sql.parser.sql.common.segment.dml.item.ProjectionSegment;
import org.apache.shardingsphere.sql.parser.sql.common.segment.generic.table.JoinTableSegment;
import org.apache.shardingsphere.sql.parser.sql.common.segment.generic.table.SimpleTableSegment;
import org.apache.shardingsphere.sql.parser.sql.common.segment.generic.table.TableSegment;
import org.apache.shardingsphere.sql.parser.sql.common.statement.SQLStatement;
import org.apache.shardingsphere.sql.parser.sql.common.statement.dml.InsertStatement;
import org.apache.shardingsphere.sql.parser.sql.common.statement.dml.SelectStatement;

/**
 * Apache ShardingSphere SQL parser, MySQL dialect: SQLParserEngine("MySQL").parse(local SQL text) returns the ANTLR
 * parse tree, and SQLVisitorEngine("MySQL", "STATEMENT") turns it into a SQLStatement (the documented two-step API).
 * Every summary field is read from that statement's segments (projections, join tables, where/group by/order by,
 * insert columns and values, aggregation, function and literal expression segments).
 */
public final class SqlHarness {
    private static final SQLParserEngine PARSER = new SQLParserEngine("MySQL", new CacheOption(128, 1024L));
    private static final SQLVisitorEngine VISITOR = new SQLVisitorEngine("MySQL", "STATEMENT", false, new Properties());

    private static final class Summary {
        final TreeSet<String> tables = new TreeSet<>();
        final TreeSet<String> functions = new TreeSet<>();
        final List<String[]> literals = new ArrayList<>();
        int joins = 0;

        void table(TableSegment segment) {
            if (segment instanceof JoinTableSegment join) {
                joins++;
                table(join.getLeft());
                table(join.getRight());
                if (join.getCondition() != null) expression(join.getCondition());
            } else if (segment instanceof SimpleTableSegment simple) {
                tables.add(simple.getTableName().getIdentifier().getValue().toLowerCase(Locale.ROOT));
            }
        }

        void projection(ProjectionSegment segment) {
            if (segment instanceof AggregationProjectionSegment aggregation) {
                functions.add(aggregation.getType().name().toLowerCase(Locale.ROOT));
                for (ExpressionSegment parameter : aggregation.getParameters()) expression(parameter);
            } else if (segment instanceof ExpressionProjectionSegment projection && projection.getExpr() != null) {
                expression(projection.getExpr());
            }
        }

        void expression(ExpressionSegment segment) {
            if (segment instanceof BinaryOperationExpression binary) {
                expression(binary.getLeft());
                expression(binary.getRight());
            } else if (segment instanceof FunctionSegment function) {
                functions.add(function.getFunctionName().toLowerCase(Locale.ROOT));
                for (ExpressionSegment parameter : function.getParameters()) expression(parameter);
            } else if (segment instanceof LiteralExpressionSegment literal && literal.getLiterals() != null) {
                Object value = literal.getLiterals();
                if (value instanceof String text) literals.add(new String[]{"string", text});
                else if (value instanceof BigDecimal decimal) literals.add(new String[]{"number", decimal.toPlainString()});
                else if (value instanceof Number number) literals.add(new String[]{"number", number.toString()});
            }
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

    static String summarize(SQLStatement statement) {
        Summary summary = new Summary();
        if (statement instanceof SelectStatement select) {
            if (select.getFrom() != null) summary.table(select.getFrom());
            for (ProjectionSegment projection : select.getProjections().getProjections()) summary.projection(projection);
            select.getWhere().ifPresent(where -> summary.expression(where.getExpr()));
            int groupBy = select.getGroupBy().map(group -> group.getGroupByItems().size()).orElse(0);
            int orderBy = select.getOrderBy().map(order -> order.getOrderByItems().size()).orElse(0);
            return "{\"kind\":\"select\",\"tables\":" + names(summary.tables)
                    + ",\"select_items\":" + select.getProjections().getProjections().size()
                    + ",\"joins\":" + summary.joins
                    + ",\"where\":" + select.getWhere().isPresent()
                    + ",\"group_by\":" + groupBy + ",\"order_by\":" + orderBy
                    + ",\"functions\":" + names(summary.functions)
                    + ",\"literals\":" + summary.literalJson() + "}";
        }
        if (statement instanceof InsertStatement insert && !insert.getValues().isEmpty()) {
            summary.table(insert.getTable());
            for (InsertValuesSegment row : insert.getValues()) {
                for (ExpressionSegment value : row.getValues()) summary.expression(value);
            }
            return "{\"kind\":\"insert\",\"tables\":" + names(summary.tables)
                    + ",\"columns\":" + insert.getInsertColumns().map(columns -> columns.getColumns().size()).orElse(0)
                    + ",\"rows\":" + insert.getValues().size()
                    + ",\"literals\":" + summary.literalJson() + "}";
        }
        return "{\"kind\":" + quote(statement.getClass().getSimpleName().toLowerCase(Locale.ROOT)) + "}";
    }

    static String parse(byte[] data) throws CharacterCodingException {
        if (data.length == 0 || data.length > (1 << 20)) throw new IllegalArgumentException("input outside harness limit");
        String text = StandardCharsets.UTF_8.newDecoder()
                .onMalformedInput(CodingErrorAction.REPORT)
                .onUnmappableCharacter(CodingErrorAction.REPORT)
                .decode(ByteBuffer.wrap(data)).toString();
        ParseASTNode tree = PARSER.parse(text, false);
        SQLStatement statement = VISITOR.visit(tree);
        return "{\"statement_count\":1,\"statements\":[" + summarize(statement) + "]}";
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (SQLParsingException | IllegalArgumentException | CharacterCodingException rejected) { }
    }

    public static void main(String[] args) throws Exception {
        System.out.println(parse(Files.readAllBytes(Path.of(args[0]))));
    }
}
