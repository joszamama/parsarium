package org.parsarium;

import io.github.wasabithumb.jtoml.JToml;
import io.github.wasabithumb.jtoml.document.TomlDocument;
import io.github.wasabithumb.jtoml.key.TomlKey;
import io.github.wasabithumb.jtoml.value.TomlValue;
import io.github.wasabithumb.jtoml.value.array.TomlArray;
import io.github.wasabithumb.jtoml.value.primitive.TomlPrimitive;
import io.github.wasabithumb.jtoml.value.table.TomlTable;
import java.math.BigDecimal;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public final class TomlAdapter {
    private TomlAdapter() { }

    // Parse one local TOML file with JToml.jToml().read(Path) and print the typed tree of the
    // returned TomlDocument. Parse errors are thrown as TomlParseException.
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("jtoml")) System.exit(2);
        TomlDocument document = JToml.jToml().read(Path.of(args[1]));
        System.out.println(typed(document));
    }

    private static String typed(TomlValue value) {
        if (value.isTable()) {
            TomlTable table = value.asTable();
            Map<String, String> fields = new TreeMap<>();
            for (TomlKey key : table.keys(false)) {
                if (key.size() != 1) throw new IllegalStateException("unexpected multi-part key " + key);
                String name = key.get(0);
                if (fields.put(name, typed(table.get(key))) != null)
                    throw new IllegalStateException("duplicate key " + name);
            }
            List<String> parts = new ArrayList<>();
            for (Map.Entry<String, String> entry : fields.entrySet())
                parts.add(quote(entry.getKey()) + ":" + entry.getValue());
            return "{" + String.join(",", parts) + "}";
        }
        if (value.isArray()) {
            TomlArray array = value.asArray();
            List<String> parts = new ArrayList<>();
            for (int index = 0; index < array.size(); index++) parts.add(typed(array.get(index)));
            return "[" + String.join(",", parts) + "]";
        }
        TomlPrimitive primitive = value.asPrimitive();
        if (primitive.isString()) return scalar("string", primitive.asString());
        if (primitive.isBoolean()) return scalar("bool", primitive.asBoolean() ? "true" : "false");
        if (primitive.isInteger()) return scalar("integer", Long.toString(primitive.asLong()));
        if (primitive.isFloat()) return scalar("float", floatText(primitive.asDouble()));
        if (primitive.isOffsetDateTime())
            return scalar("datetime", dateTime(primitive.asOffsetDateTime()
                    .withOffsetSameInstant(ZoneOffset.UTC).toLocalDateTime()) + "Z");
        if (primitive.isLocalDateTime()) return scalar("datetime-local", dateTime(primitive.asLocalDateTime()));
        if (primitive.isLocalDate()) return scalar("date-local", primitive.asLocalDate().toString());
        if (primitive.isLocalTime()) return scalar("time-local", timeText(primitive.asLocalTime()));
        throw new IllegalStateException("unsupported TOML primitive " + primitive.type());
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

    private static String scalar(String type, String value) {
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
