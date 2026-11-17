package org.parsarium;

import com.electronwill.nightconfig.core.CommentedConfig;
import com.electronwill.nightconfig.core.UnmodifiableConfig;
import com.electronwill.nightconfig.toml.TomlParser;
import java.io.Reader;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
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

    // Parse one local UTF-8 TOML file with new TomlParser().parse(Reader) and print the typed tree
    // of the returned CommentedConfig (sub-tables are Config, arrays are List, scalars are Java values).
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("night-config-toml")) System.exit(2);
        CommentedConfig result;
        try (Reader reader = Files.newBufferedReader(Path.of(args[1]), StandardCharsets.UTF_8)) {
            result = new TomlParser().parse(reader);
        }
        System.out.println(typed(result));
    }

    private static String typed(Object value) {
        if (value instanceof UnmodifiableConfig table) {
            Map<String, String> fields = new TreeMap<>();
            for (UnmodifiableConfig.Entry entry : table.entrySet())
                fields.put(entry.getKey(), typed(entry.getRawValue()));
            List<String> parts = new ArrayList<>();
            for (Map.Entry<String, String> entry : fields.entrySet())
                parts.add(quote(entry.getKey()) + ":" + entry.getValue());
            return "{" + String.join(",", parts) + "}";
        }
        if (value instanceof List<?> array) {
            List<String> parts = new ArrayList<>();
            for (Object item : array) parts.add(typed(item));
            return "[" + String.join(",", parts) + "]";
        }
        if (value instanceof String text) return scalar("string", text);
        if (value instanceof Boolean flag) return scalar("bool", flag ? "true" : "false");
        if (value instanceof Long number) return scalar("integer", number.toString());
        if (value instanceof Integer number) return scalar("integer", number.toString());
        if (value instanceof Double number) return scalar("float", floatText(number));
        if (value instanceof OffsetDateTime time)
            return scalar("datetime", dateTime(time.withOffsetSameInstant(ZoneOffset.UTC).toLocalDateTime()) + "Z");
        if (value instanceof LocalDateTime time) return scalar("datetime-local", dateTime(time));
        if (value instanceof LocalDate date) return scalar("date-local", date.toString());
        if (value instanceof LocalTime time) return scalar("time-local", timeText(time));
        throw new IllegalStateException("unsupported TOML value " + (value == null ? "null" : value.getClass().getName()));
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
