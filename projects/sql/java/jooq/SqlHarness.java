import java.lang.reflect.Method;
import java.math.BigDecimal;
import java.nio.charset.CharacterCodingException;
import java.nio.charset.CodingErrorAction;
import java.nio.charset.StandardCharsets;
import java.nio.ByteBuffer;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.TreeSet;
import org.jooq.AggregateFunction;
import org.jooq.DSLContext;
import org.jooq.Named;
import org.jooq.Param;
import org.jooq.Queries;
import org.jooq.Query;
import org.jooq.Row;
import org.jooq.SQLDialect;
import org.jooq.Select;
import org.jooq.Table;
import org.jooq.conf.Settings;
import org.jooq.impl.DSL;
import org.jooq.impl.QOM;

/**
 * jOOQ parser (DSLContext.parser().parse) over local SQL text with SQLDialect.DEFAULT.
 * Every summary field is read from jOOQ's query object model (QOM); the text is not inspected.
 */
public final class SqlHarness {
    private static final DSLContext CONTEXT = DSL.using(SQLDialect.DEFAULT,
            new Settings().withRenderSchema(false));

    private static final class Walk {
        final TreeSet<String> tables = new TreeSet<>();
        final TreeSet<String> functions = new TreeSet<>();
        final List<String[]> literals = new ArrayList<>();
        int joins;

        void visit(Object part) throws Exception {
            if (part == null) return;
            if (part instanceof Collection<?> items) {
                for (Object item : items) visit(item);
                return;
            }
            if (part instanceof Param<?> param) {
                Object value = param.getValue();
                if (value instanceof String text) literals.add(new String[]{"string", text});
                else if (value instanceof BigDecimal decimal) literals.add(new String[]{"number", decimal.toPlainString()});
                else if (value instanceof Number number) literals.add(new String[]{"number", number.toString()});
                return;
            }
            if (part instanceof QOM.Join<?> join) {
                joins++;
                visit(join.$table1());
                visit(join.$table2());
                visit(join.$on());
                return;
            }
            if (part instanceof QOM.TableAlias<?> alias) { visit(alias.$table()); return; }
            if (part instanceof QOM.FieldAlias<?> alias) { visit(alias.$field()); return; }
            if (part instanceof QOM.Count count) { functions.add("count"); visit(count.$field()); return; }
            if (part instanceof QOM.Sum sum) { functions.add("sum"); visit(sum.$field()); return; }
            if (part instanceof AggregateFunction<?> && part instanceof Named named) {
                functions.add(named.getName().toLowerCase());
            }
            if (part instanceof Row row) { visit(row.$fields()); return; }
            // Aliases and joins are unwrapped above; a remaining table reference is a base table.
            if (part instanceof Table<?> table) { tables.add(table.getName().toLowerCase()); return; }
            Method args = argsMethod(part);
            if (args != null) visit(args.invoke(part));
        }

        // QOM operators (And, Eq, Ge, ...) expose their operands through $args().
        private static Method argsMethod(Object part) {
            try {
                Method method = part.getClass().getMethod("$args");
                method.setAccessible(true);
                return method;
            } catch (NoSuchMethodException | SecurityException missing) {
                return null;
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

    static String summarize(Query query) throws Exception {
        Walk walk = new Walk();
        if (query instanceof Select<?> select) {
            walk.visit(select.$select());
            walk.visit(select.$from());
            walk.visit(select.$where());
            walk.visit(select.$groupBy());
            walk.visit(select.$orderBy());
            return "{\"kind\":\"select\",\"tables\":" + names(walk.tables)
                    + ",\"select_items\":" + select.$select().size()
                    + ",\"joins\":" + walk.joins
                    + ",\"where\":" + (select.$where() != null)
                    + ",\"group_by\":" + select.$groupBy().size()
                    + ",\"order_by\":" + select.$orderBy().size()
                    + ",\"functions\":" + names(walk.functions)
                    + ",\"literals\":" + walk.literalJson() + "}";
        }
        if (query instanceof QOM.Insert<?> insert) {
            walk.visit(insert.$into());
            for (Row row : insert.$values()) walk.visit(row);
            return "{\"kind\":\"insert\",\"tables\":" + names(walk.tables)
                    + ",\"columns\":" + insert.$columns().size()
                    + ",\"rows\":" + insert.$values().size()
                    + ",\"literals\":" + walk.literalJson() + "}";
        }
        return "{\"kind\":" + quote(query.getClass().getSimpleName().toLowerCase()) + "}";
    }

    static String parse(byte[] data) throws Exception {
        if (data.length == 0 || data.length > (1 << 20)) throw new IllegalArgumentException("input outside harness limit");
        String text = StandardCharsets.UTF_8.newDecoder()
                .onMalformedInput(CodingErrorAction.REPORT)
                .onUnmappableCharacter(CodingErrorAction.REPORT)
                .decode(ByteBuffer.wrap(data)).toString();
        Queries queries = CONTEXT.parser().parse(text);
        List<String> statements = new ArrayList<>();
        for (Query query : queries) statements.add(summarize(query));
        return "{\"statement_count\":" + statements.size() + ",\"statements\":[" + String.join(",", statements) + "]}";
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (org.jooq.impl.ParserException | IllegalArgumentException | CharacterCodingException rejected) { }
        catch (RuntimeException error) { throw error; }
        catch (Exception ignored) { }
    }

    public static void main(String[] args) throws Exception {
        System.setProperty("org.jooq.no-logo", "true");
        System.setProperty("org.jooq.no-tips", "true");
        System.out.println(parse(Files.readAllBytes(Path.of(args[0]))));
    }
}
