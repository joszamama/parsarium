package org.parsarium;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.POJONode;
import com.fasterxml.jackson.dataformat.toml.TomlMapper;
import com.fasterxml.jackson.dataformat.toml.TomlReadFeature;
import java.math.BigDecimal;
import java.nio.file.Path;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public final class TomlAdapter {
    private TomlAdapter() { }

    // Read one local TOML file with TomlMapper.readTree(File) and print the typed tree of the
    // returned JsonNode. PARSE_JAVA_TIME is enabled so TOML date/time values arrive as java.time
    // objects in POJONodes; without it they are TextNodes, indistinguishable from strings.
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("jackson-dataformat-toml")) System.exit(2);
        TomlMapper mapper = TomlMapper.builder().enable(TomlReadFeature.PARSE_JAVA_TIME).build();
        JsonNode root = mapper.readTree(Path.of(args[1]).toFile());
        if (root == null || !root.isObject()) throw new IllegalArgumentException("TOML root is not a table");
        System.out.println(typed(root));
    }

    private static String typed(JsonNode node) {
        if (node.isObject()) {
            Map<String, String> fields = new TreeMap<>();
            for (Map.Entry<String, JsonNode> entry : node.properties())
                fields.put(entry.getKey(), typed(entry.getValue()));
            List<String> parts = new ArrayList<>();
            for (Map.Entry<String, String> entry : fields.entrySet())
                parts.add(quote(entry.getKey()) + ":" + entry.getValue());
            return "{" + String.join(",", parts) + "}";
        }
        if (node.isArray()) {
            List<String> parts = new ArrayList<>();
            for (JsonNode item : node) parts.add(typed(item));
            return "[" + String.join(",", parts) + "]";
        }
        if (node.isTextual()) return scalar("string", node.textValue());
        if (node.isBoolean()) return scalar("bool", node.booleanValue() ? "true" : "false");
        if (node.isIntegralNumber()) return scalar("integer", node.bigIntegerValue().toString());
        // Floats arrive as DecimalNode (BigDecimal); TOML floats are binary64, so take doubleValue().
        if (node.isFloatingPointNumber()) return scalar("float", floatText(node.doubleValue()));
        if (node instanceof POJONode pojo) {
            Object value = pojo.getPojo();
            if (value instanceof OffsetDateTime time)
                return scalar("datetime", dateTime(time.withOffsetSameInstant(ZoneOffset.UTC).toLocalDateTime()) + "Z");
            if (value instanceof LocalDateTime time) return scalar("datetime-local", dateTime(time));
            if (value instanceof LocalDate date) return scalar("date-local", date.toString());
            if (value instanceof LocalTime time) return scalar("time-local", timeText(time));
        }
        throw new IllegalStateException("unsupported TOML node " + node.getNodeType() + " " + node.getClass().getName());
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
