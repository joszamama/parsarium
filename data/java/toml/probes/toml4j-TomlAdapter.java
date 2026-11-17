package org.parsarium;

import com.moandjiezana.toml.Toml;
import java.io.File;
import java.math.BigDecimal;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public final class TomlAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("toml4j")) System.exit(2);
        Map<String, Object> root = new Toml().read(new File(args[1])).toMap();
        System.out.println(typed(root));
    }

    private static String typed(Object value) {
        if (value instanceof Map<?, ?> map) {
            Map<String, String> fields = new TreeMap<>();
            for (Map.Entry<?, ?> e : map.entrySet()) fields.put((String) e.getKey(), typed(e.getValue()));
            List<String> parts = new ArrayList<>();
            for (Map.Entry<String, String> e : fields.entrySet()) parts.add(quote(e.getKey()) + ":" + e.getValue());
            return "{" + String.join(",", parts) + "}";
        }
        if (value instanceof List<?> list) {
            List<String> parts = new ArrayList<>();
            for (Object item : list) parts.add(typed(item));
            return "[" + String.join(",", parts) + "]";
        }
        if (value instanceof String s) return scalar("string", s);
        if (value instanceof Boolean b) return scalar("bool", b.toString());
        if (value instanceof Long l) return scalar("integer", l.toString());
        if (value instanceof Double d) { String f = new BigDecimal(Double.toString(d)).toPlainString(); if (!f.contains(".")) f += ".0"; else { f = f.replaceAll("0+$", ""); if (f.endsWith(".")) f += "0"; } return scalar("float", f); }
        if (value instanceof Date d) {
            LocalDateTime t = LocalDateTime.ofInstant(d.toInstant(), ZoneOffset.UTC);
            return scalar("datetime", t.toLocalDate() + "T" + String.format("%02d:%02d:%02d", t.getHour(), t.getMinute(), t.getSecond()) + (t.getNano() == 0 ? "" : "." + String.format("%09d", t.getNano()).replaceAll("0+$", "")) + "Z");
        }
        throw new IllegalStateException("unsupported " + value.getClass());
    }

    private static String scalar(String type, String value) {
        return "{\"type\":" + quote(type) + ",\"value\":" + quote(value) + "}";
    }

    private static String quote(String value) {
        StringBuilder out = new StringBuilder("\"");
        for (char c : value.toCharArray()) {
            switch (c) {
                case '"' -> out.append("\\\"");
                case '\\' -> out.append("\\\\");
                case '\n' -> out.append("\\n");
                case '\t' -> out.append("\\t");
                default -> out.append(c);
            }
        }
        return out.append('"').toString();
    }
}
