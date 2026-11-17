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
import org.antlr.runtime.tree.Tree;
import org.apache.hadoop.hive.ql.parse.ASTNode;
import org.apache.hadoop.hive.ql.parse.HiveParser;
import org.apache.hadoop.hive.ql.parse.ParseDriver;
import org.apache.hadoop.hive.ql.parse.ParseException;

/**
 * Apache Hive SQL parser: new ParseDriver().parse(local SQL text without its terminating semicolon).getTree().
 * Hive's grammar parses one statement followed by EOF (the Hive CLI and Beeline split on ';' before parsing);
 * the adapter removes one trailing ';' and trailing whitespace and nothing else.
 * Every summary field is read from the ANTLR ASTNode tree by token type (TOK_TABNAME, TOK_SELEXPR, join tokens,
 * TOK_WHERE, TOK_GROUPBY, TOK_ORDERBY, TOK_FUNCTION*, TOK_TABCOLNAME, Number and StringLiteral).
 */
public final class SqlHarness {
    private static final class Summary {
        final TreeSet<String> tables = new TreeSet<>();
        final TreeSet<String> functions = new TreeSet<>();
        final List<String[]> literals = new ArrayList<>();
        int selectItems = 0, joins = 0, groupBy = 0, orderBy = 0, columns = 0, rows = 0;
        boolean where = false, from = false, insertInto = false;

        void walk(Tree node) {
            int type = node.getType();
            switch (type) {
                case HiveParser.TOK_TABNAME -> {
                    List<String> parts = new ArrayList<>();
                    for (int i = 0; i < node.getChildCount(); i++) parts.add(node.getChild(i).getText());
                    tables.add(String.join(".", parts).toLowerCase(Locale.ROOT));
                }
                case HiveParser.TOK_FROM -> from = true;
                case HiveParser.TOK_INSERT_INTO -> insertInto = true;
                case HiveParser.TOK_SELEXPR -> selectItems++;
                case HiveParser.TOK_WHERE -> where = true;
                case HiveParser.TOK_GROUPBY -> groupBy = node.getChildCount();
                case HiveParser.TOK_ORDERBY -> orderBy = node.getChildCount();
                case HiveParser.TOK_TABCOLNAME -> columns = node.getChildCount();
                case HiveParser.TOK_FUNCTION, HiveParser.TOK_FUNCTIONSTAR, HiveParser.TOK_FUNCTIONDI -> {
                    String function = node.getChild(0).getText().toLowerCase(Locale.ROOT);
                    functions.add(function);
                    // Hive's grammar rewrites VALUES rows into inline(array(struct(row)...)).
                    if (function.equals("struct") && node.getParent() != null && node.getParent().getChildCount() > 0
                            && node.getParent().getChild(0).getText().equalsIgnoreCase("array")) rows++;
                }
                case HiveParser.Number -> literals.add(new String[]{"number", node.getText()});
                case HiveParser.StringLiteral -> {
                    String text = node.getText();
                    literals.add(new String[]{"string", text.substring(1, text.length() - 1)});
                }
                case HiveParser.TOK_JOIN, HiveParser.TOK_LEFTOUTERJOIN, HiveParser.TOK_RIGHTOUTERJOIN,
                        HiveParser.TOK_FULLOUTERJOIN, HiveParser.TOK_CROSSJOIN, HiveParser.TOK_LEFTSEMIJOIN,
                        HiveParser.TOK_LEFTANTISEMIJOIN, HiveParser.TOK_UNIQUEJOIN -> joins++;
                default -> { }
            }
            for (int i = 0; i < node.getChildCount(); i++) walk(node.getChild(i));
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

    static String summarize(ASTNode tree) {
        Summary summary = new Summary();
        summary.walk(tree);
        if (summary.insertInto && !summary.from) {
            return "{\"kind\":\"insert\",\"tables\":" + names(summary.tables)
                    + ",\"columns\":" + summary.columns
                    + ",\"rows\":" + summary.rows
                    + ",\"literals\":" + summary.literalJson() + "}";
        }
        if (summary.from) {
            return "{\"kind\":\"select\",\"tables\":" + names(summary.tables)
                    + ",\"select_items\":" + summary.selectItems
                    + ",\"joins\":" + summary.joins
                    + ",\"where\":" + summary.where
                    + ",\"group_by\":" + summary.groupBy + ",\"order_by\":" + summary.orderBy
                    + ",\"functions\":" + names(summary.functions)
                    + ",\"literals\":" + summary.literalJson() + "}";
        }
        Tree first = tree.getChildCount() > 0 ? tree.getChild(0) : tree;
        return "{\"kind\":" + quote(first.getText().toLowerCase(Locale.ROOT)) + "}";
    }

    static String parse(byte[] data) throws CharacterCodingException, ParseException {
        if (data.length == 0 || data.length > (1 << 20)) throw new IllegalArgumentException("input outside harness limit");
        String text = StandardCharsets.UTF_8.newDecoder()
                .onMalformedInput(CodingErrorAction.REPORT)
                .onUnmappableCharacter(CodingErrorAction.REPORT)
                .decode(ByteBuffer.wrap(data)).toString().stripTrailing();
        if (text.endsWith(";")) text = text.substring(0, text.length() - 1);
        ASTNode tree = new ParseDriver().parse(text).getTree();
        return "{\"statement_count\":1,\"statements\":[" + summarize(tree) + "]}";
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (ParseException | IllegalArgumentException | CharacterCodingException rejected) { }
    }

    public static void main(String[] args) throws Exception {
        System.out.println(parse(Files.readAllBytes(Path.of(args[0]))));
    }
}
