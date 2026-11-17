package org.parsarium;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public final class JsonAdapter {
    private JsonAdapter() { }

    private static final class Summary {
        int objects, arrays, booleans, nulls, depth;
        final List<String> strings = new ArrayList<>();
        final List<Double> numbers = new ArrayList<>();
    }

    // Parses local UTF-8 bytes with json-smart JSONParser in RFC4627 mode,
    // then prints a structural summary without another JSON library.
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("json-smart")) System.exit(2);
        Object root = new net.minidev.json.parser.JSONParser(
                net.minidev.json.parser.JSONParser.MODE_RFC4627)
                .parse(Files.readAllBytes(Path.of(args[1])));
        Summary summary = new Summary();
        walk(root, 0, summary);
        Collections.sort(summary.strings);
        Collections.sort(summary.numbers);
        Map<String, String> result = new TreeMap<>();
        result.put("objects", Integer.toString(summary.objects));
        result.put("arrays", Integer.toString(summary.arrays));
        result.put("booleans", Integer.toString(summary.booleans));
        result.put("nulls", Integer.toString(summary.nulls));
        result.put("max_depth", Integer.toString(summary.depth));
        List<String> strings = new ArrayList<>();
        for (String value : summary.strings) strings.add(quote(value));
        result.put("strings", "[" + String.join(",", strings) + "]");
        List<String> numbers = new ArrayList<>();
        for (Double value : summary.numbers) numbers.add(number(value));
        result.put("numbers", "[" + String.join(",", numbers) + "]");
        if (root instanceof Map<?, ?> map) {
            List<String> keys = new ArrayList<>();
            for (Object key : map.keySet()) keys.add((String) key);
            Collections.sort(keys);
            List<String> quoted = new ArrayList<>();
            for (String key : keys) quoted.add(quote(key));
            result.put("root", quote("object"));
            result.put("top_level_keys", "[" + String.join(",", quoted) + "]");
        } else if (root instanceof List<?> list) {
            result.put("root", quote("array"));
            result.put("top_level_items", Integer.toString(list.size()));
        } else {
            result.put("root", quote("scalar"));
        }
        List<String> parts = new ArrayList<>();
        for (Map.Entry<String, String> entry : result.entrySet()) {
            parts.add(quote(entry.getKey()) + ":" + entry.getValue());
        }
        System.out.println("{" + String.join(",", parts) + "}");
    }

    private static void walk(Object value, int level, Summary summary) {
        if (value instanceof Map<?, ?> map) {
            summary.objects++;
            summary.depth = Math.max(summary.depth, level + 1);
            for (Object child : map.values()) walk(child, level + 1, summary);
        } else if (value instanceof List<?> list) {
            summary.arrays++;
            summary.depth = Math.max(summary.depth, level + 1);
            for (Object child : list) walk(child, level + 1, summary);
        } else if (value instanceof String text) {
            summary.strings.add(text);
        } else if (value instanceof Number number) {
            summary.numbers.add(number.doubleValue());
        } else if (value instanceof Boolean) {
            summary.booleans++;
        } else if (value == null) {
            summary.nulls++;
        } else {
            throw new IllegalStateException("unexpected node " + value.getClass());
        }
    }

    private static String number(double value) {
        if (value == Math.rint(value) && Math.abs(value) < 1e15) return Long.toString((long) value);
        return Double.toString(value);
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
                default -> {
                    if (c < 0x20) out.append(String.format("\\u%04x", (int) c));
                    else out.append(c);
                }
            }
        }
        return out.append('"').toString();
    }
}
