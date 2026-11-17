package org.parsarium;

import java.io.InputStream;
import java.math.BigInteger;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import it.krzeminski.snakeyaml.engine.kmp.api.Load;
import it.krzeminski.snakeyaml.engine.kmp.api.LoadSettings;

public final class YamlAdapter {
    private YamlAdapter() { }

    // Load one local YAML document with Load(LoadSettings()).loadOne(InputStream); 5.0.0 defaults to CoreSchema.
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("snakeyaml-engine-kmp")) System.exit(2);
        Load load = new Load(new LoadSettings());
        Object root;
        try (InputStream input = Files.newInputStream(Path.of(args[1]))) {
            root = load.loadOne(input);
        }
        StringBuilder out = new StringBuilder();
        tree(root, out);
        System.out.println("{\"tree\":" + out + "}");
    }

    private static void tree(Object node, StringBuilder out) throws java.io.IOException {
        if (node instanceof Map<?, ?> map) {
            out.append("[\"map\",[");
            boolean first = true;
            for (Map.Entry<?, ?> entry : map.entrySet()) {
                if (!(entry.getKey() instanceof String key)) throw new java.io.IOException("non-string key");
                if (!first) out.append(',');
                first = false;
                out.append('[');
                quote(key, out);
                out.append(',');
                tree(entry.getValue(), out);
                out.append(']');
            }
            out.append("]]");
        } else if (node instanceof List<?> list) {
            out.append("[\"seq\",[");
            for (int index = 0; index < list.size(); index++) {
                if (index > 0) out.append(',');
                tree(list.get(index), out);
            }
            out.append("]]");
        } else if (node instanceof String text) {
            out.append("[\"str\",");
            quote(text, out);
            out.append(']');
        } else if (node instanceof Integer || node instanceof Long || node instanceof BigInteger) {
            out.append("[\"int\",\"").append(node).append("\"]");
        } else if (node instanceof Double value) {
            out.append("[\"float\",\"").append(Double.toString(value)).append("\"]");
        } else if (node instanceof Boolean value) {
            out.append("[\"bool\",").append(value).append(']');
        } else if (node == null) {
            out.append("[\"null\"]");
        } else {
            throw new java.io.IOException("unexpected value " + node.getClass().getName());
        }
    }

    private static void quote(String value, StringBuilder out) {
        out.append('"');
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
        out.append('"');
    }
}
