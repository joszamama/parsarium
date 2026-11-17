package org.parsarium;

import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonToken;
import java.io.InputStream;
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
        int objects, arrays, booleans, nulls, depth, topItems;
        String root;
        final List<String> strings = new ArrayList<>();
        final List<Double> numbers = new ArrayList<>();
        final List<String> topKeys = new ArrayList<>();
    }

    // Consume every token of one local JSON stream directly through jackson-core.
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("jackson-core")) System.exit(2);
        JsonFactory factory = JsonFactory.builder()
                .disable(JsonFactory.Feature.CANONICALIZE_FIELD_NAMES).build();
        Summary summary = new Summary();
        try (InputStream input = Files.newInputStream(Path.of(args[1]));
             JsonParser parser = factory.createParser(input)) {
            JsonToken token;
            int depth = 0;
            boolean rootFinished = false;
            while ((token = parser.nextToken()) != null) {
                if (rootFinished) throw new IllegalArgumentException("multiple JSON roots");
                if (summary.root == null) {
                    summary.root = token == JsonToken.START_OBJECT ? "object"
                            : token == JsonToken.START_ARRAY ? "array" : "scalar";
                }
                if (summary.root.equals("array") && depth == 1 && token != JsonToken.END_ARRAY)
                    summary.topItems++;
                switch (token) {
                    case START_OBJECT -> { summary.objects++; depth++; summary.depth = Math.max(summary.depth, depth); }
                    case START_ARRAY -> { summary.arrays++; depth++; summary.depth = Math.max(summary.depth, depth); }
                    case END_OBJECT, END_ARRAY -> { depth--; if (depth == 0) rootFinished = true; }
                    case FIELD_NAME -> {
                        if (depth == 1 && summary.root.equals("object"))
                            summary.topKeys.add(parser.currentName());
                    }
                    case VALUE_STRING -> summary.strings.add(parser.getText());
                    case VALUE_NUMBER_INT, VALUE_NUMBER_FLOAT -> summary.numbers.add(parser.getDoubleValue());
                    case VALUE_TRUE, VALUE_FALSE -> summary.booleans++;
                    case VALUE_NULL -> summary.nulls++;
                    default -> throw new IllegalStateException("unexpected token " + token);
                }
                if (summary.root.equals("scalar")) rootFinished = true;
            }
            if (summary.root == null || !rootFinished || depth != 0)
                throw new IllegalArgumentException("incomplete JSON document");
        }
        Collections.sort(summary.strings);
        Collections.sort(summary.numbers);
        Collections.sort(summary.topKeys);
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
        result.put("root", quote(summary.root));
        if (summary.root.equals("object")) {
            List<String> keys = new ArrayList<>();
            for (String key : summary.topKeys) keys.add(quote(key));
            result.put("top_level_keys", "[" + String.join(",", keys) + "]");
        } else if (summary.root.equals("array")) {
            result.put("top_level_items", Integer.toString(summary.topItems));
        }
        List<String> parts = new ArrayList<>();
        for (Map.Entry<String, String> entry : result.entrySet())
            parts.add(quote(entry.getKey()) + ":" + entry.getValue());
        System.out.println("{" + String.join(",", parts) + "}");
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
                default -> { if (c < 0x20) out.append(String.format("\\u%04x", (int) c)); else out.append(c); }
            }
        }
        return out.append('"').toString();
    }
}
