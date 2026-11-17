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

    // Reads a complete local document through Parsson's own JsonParserImpl.
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("parsson")) System.exit(2);
        jakarta.json.JsonValue root;
        org.eclipse.parsson.JsonProviderImpl provider = new org.eclipse.parsson.JsonProviderImpl();
        try (java.io.InputStream input = Files.newInputStream(Path.of(args[1]));
             jakarta.json.stream.JsonParser parser = provider.createParser(input)) {
            if (!parser.hasNext()) throw new IllegalArgumentException("empty JSON document");
            parser.next();
            root = parser.getValue();
            if (parser.hasNext()) throw new IllegalArgumentException("trailing JSON content");
        }
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
        if (root instanceof jakarta.json.JsonObject object) {
            List<String> keys = new ArrayList<>(object.keySet());
            Collections.sort(keys);
            List<String> quoted = new ArrayList<>();
            for (String key : keys) quoted.add(quote(key));
            result.put("root", quote("object"));
            result.put("top_level_keys", "[" + String.join(",", quoted) + "]");
        } else if (root instanceof jakarta.json.JsonArray array) {
            result.put("root", quote("array"));
            result.put("top_level_items", Integer.toString(array.size()));
        } else {
            result.put("root", quote("scalar"));
        }
        List<String> parts = new ArrayList<>();
        for (Map.Entry<String, String> entry : result.entrySet()) {
            parts.add(quote(entry.getKey()) + ":" + entry.getValue());
        }
        System.out.println("{" + String.join(",", parts) + "}");
    }

    private static void walk(jakarta.json.JsonValue value, int level, Summary summary) {
        switch (value.getValueType()) {
            case OBJECT -> {
                summary.objects++;
                summary.depth = Math.max(summary.depth, level + 1);
                for (jakarta.json.JsonValue child : ((jakarta.json.JsonObject) value).values())
                    walk(child, level + 1, summary);
            }
            case ARRAY -> {
                summary.arrays++;
                summary.depth = Math.max(summary.depth, level + 1);
                for (jakarta.json.JsonValue child : ((jakarta.json.JsonArray) value))
                    walk(child, level + 1, summary);
            }
            case STRING -> summary.strings.add(((jakarta.json.JsonString) value).getString());
            case NUMBER -> summary.numbers.add(((jakarta.json.JsonNumber) value).doubleValue());
            case TRUE, FALSE -> summary.booleans++;
            case NULL -> summary.nulls++;
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
