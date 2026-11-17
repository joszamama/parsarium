package org.parsarium;

import com.akuleshov7.ktoml.TomlInputConfig;
import com.akuleshov7.ktoml.parsers.TomlParser;
import com.akuleshov7.ktoml.tree.nodes.TableType;
import com.akuleshov7.ktoml.tree.nodes.TomlArrayOfTablesElement;
import com.akuleshov7.ktoml.tree.nodes.TomlFile;
import com.akuleshov7.ktoml.tree.nodes.TomlKeyValueArray;
import com.akuleshov7.ktoml.tree.nodes.TomlKeyValuePrimitive;
import com.akuleshov7.ktoml.tree.nodes.TomlNode;
import com.akuleshov7.ktoml.tree.nodes.TomlStubEmptyNode;
import com.akuleshov7.ktoml.tree.nodes.TomlTable;
import com.akuleshov7.ktoml.tree.nodes.pairs.values.TomlArray;
import com.akuleshov7.ktoml.tree.nodes.pairs.values.TomlBasicString;
import com.akuleshov7.ktoml.tree.nodes.pairs.values.TomlBoolean;
import com.akuleshov7.ktoml.tree.nodes.pairs.values.TomlDateTime;
import com.akuleshov7.ktoml.tree.nodes.pairs.values.TomlDouble;
import com.akuleshov7.ktoml.tree.nodes.pairs.values.TomlLiteralString;
import com.akuleshov7.ktoml.tree.nodes.pairs.values.TomlLong;
import com.akuleshov7.ktoml.tree.nodes.pairs.values.TomlValue;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import kotlinx.datetime.ConvertersKt;

public final class TomlAdapter {
    private TomlAdapter() { }

    // ktoml's documented AST entry (README "Parser to AST"; KDoc on TomlParser.parseString) is
    // TomlParser(TomlInputConfig()).parseString(String). TomlParser is a Kotlin @JvmInline value
    // class, so Kotlin callers compile that call to the public static parseString-impl(config, text);
    // Java has no source syntax for the mangled name and reaches the same method by reflection.
    private static final Method PARSE_STRING;
    static {
        try {
            PARSE_STRING = TomlParser.class.getMethod("parseString-impl", TomlInputConfig.class, String.class);
        } catch (NoSuchMethodException error) {
            throw new ExceptionInInitializerError(error);
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("ktoml-core")) System.exit(2);
        String text = new String(Files.readAllBytes(Path.of(args[1])), StandardCharsets.UTF_8);
        TomlFile file;
        try {
            file = (TomlFile) PARSE_STRING.invoke(null, new TomlInputConfig(), text);
        } catch (InvocationTargetException error) {
            Throwable cause = error.getCause();
            if (cause instanceof Exception checked) throw checked;
            if (cause instanceof Error failure) throw failure;
            throw error;
        }
        System.out.println(table(file));
    }

    // A table-like node (TomlFile, TomlTable, TomlArrayOfTablesElement): its children are key-value
    // pairs, sub-tables and arrays of tables, keyed by TomlNode.getName(), the unquoted TOML name
    // the library's own decoders (TomlMainDecoder, TomlMapDecoder) match. For a dotted key-value the
    // parser moves the prefix into synthetic tables and re-splits the remaining TomlKey, so
    // getKey().last() of site."example.com" is "com"; the node name keeps "example.com".
    private static String table(TomlNode node) {
        Map<String, String> fields = new TreeMap<>();
        for (TomlNode child : node.getChildren()) {
            if (child instanceof TomlStubEmptyNode) continue;
            String name;
            String value;
            if (child instanceof TomlKeyValuePrimitive pair) {
                name = pair.getName();
                value = scalar(pair.getValue());
            } else if (child instanceof TomlKeyValueArray pair) {
                name = pair.getName();
                value = array(pair.getValue());
            } else if (child instanceof TomlTable sub && sub.getType() == TableType.PRIMITIVE) {
                name = sub.getName();
                value = table(sub);
            } else if (child instanceof TomlTable sub && sub.getType() == TableType.ARRAY) {
                name = sub.getName();
                List<String> elements = new ArrayList<>();
                for (TomlNode element : sub.getChildren()) {
                    if (!(element instanceof TomlArrayOfTablesElement)) {
                        throw new IllegalStateException("unexpected array-of-tables child " + element.getClass());
                    }
                    elements.add(table(element));
                }
                value = "[" + String.join(",", elements) + "]";
            } else {
                throw new IllegalStateException("unexpected node " + child.getClass().getName());
            }
            if (fields.put(name, value) != null) throw new IllegalStateException("duplicate key " + name);
        }
        List<String> parts = new ArrayList<>();
        for (Map.Entry<String, String> entry : fields.entrySet()) parts.add(quote(entry.getKey()) + ":" + entry.getValue());
        return "{" + String.join(",", parts) + "}";
    }

    private static String array(TomlValue value) {
        if (!(value instanceof TomlArray array)) throw new IllegalStateException("array pair without TomlArray");
        List<String> parts = new ArrayList<>();
        for (Object element : (List<?>) array.getContent()) {
            if (element instanceof TomlArray nested) parts.add(array(nested));
            else if (element instanceof TomlValue scalar) parts.add(scalar(scalar));
            else throw new IllegalStateException("unexpected array element " + element.getClass().getName());
        }
        return "[" + String.join(",", parts) + "]";
    }

    // Type-tags one ktoml value node by its class and the library's own content object.
    private static String scalar(TomlValue value) {
        Object content = value.getContent();
        if (value instanceof TomlBasicString || value instanceof TomlLiteralString)
            return tagged("string", (String) content);
        if (value instanceof TomlBoolean) return tagged("bool", ((Boolean) content) ? "true" : "false");
        if (value instanceof TomlLong) return tagged("integer", Long.toString((Long) content));
        if (value instanceof TomlDouble) return tagged("float", floatText((Double) content));
        if (value instanceof TomlDateTime) {
            if (content instanceof kotlin.time.Instant instant) {
                Instant utc = Instant.ofEpochSecond(instant.getEpochSeconds(), instant.getNanosecondsOfSecond());
                return tagged("datetime", dateTime(LocalDateTime.ofInstant(utc, ZoneOffset.UTC)) + "Z");
            }
            if (content instanceof kotlinx.datetime.LocalDateTime local)
                return tagged("datetime-local", dateTime(ConvertersKt.toJavaLocalDateTime(local)));
            if (content instanceof kotlinx.datetime.LocalDate date)
                return tagged("date-local", ConvertersKt.toJavaLocalDate(date).toString());
            if (content instanceof kotlinx.datetime.LocalTime time)
                return tagged("time-local", timeText(ConvertersKt.toJavaLocalTime(time)));
            throw new IllegalStateException("unexpected date-time content " + content.getClass().getName());
        }
        throw new IllegalStateException("unsupported TOML value " + value.getClass().getName());
    }

    // Shortest round-trip digits of the binary64 value, written positionally with a fractional digit.
    private static String floatText(double value) {
        if (Double.isNaN(value) || Double.isInfinite(value)) throw new IllegalStateException("non-finite float");
        String text = new BigDecimal(Double.toString(value)).toPlainString();
        if (!text.contains(".")) return text + ".0";
        text = text.replaceAll("0+$", "");
        return text.endsWith(".") ? text + "0" : text;
    }

    private static String dateTime(LocalDateTime value) {
        return value.toLocalDate() + "T" + timeText(value.toLocalTime());
    }

    private static String timeText(LocalTime value) {
        String text = String.format("%02d:%02d:%02d", value.getHour(), value.getMinute(), value.getSecond());
        int nanos = value.getNano();
        return nanos == 0 ? text : text + "." + String.format("%09d", nanos).replaceAll("0+$", "");
    }

    private static String tagged(String type, String value) {
        return "{\"type\":" + quote(type) + ",\"value\":" + quote(value) + "}";
    }

    private static String quote(String value) {
        StringBuilder out = new StringBuilder("\"");
        for (int index = 0; index < value.length(); index++) {
            char c = value.charAt(index);
            switch (c) {
                case '"' -> out.append("\\\"");
                case '\\' -> out.append("\\\\");
                case '\n' -> out.append("\\n");
                case '\r' -> out.append("\\r");
                case '\t' -> out.append("\\t");
                default -> { if (c < 0x20) out.append(String.format("\\u%04x", (int) c)); else out.append(c); }
            }
        }
        return out.append('"').toString();
    }
}
