package org.parsarium;

import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;
import io.kjson.JSONArray;
import io.kjson.JSONBoolean;
import io.kjson.JSONDecimal;
import io.kjson.JSONInt;
import io.kjson.JSONLong;
import io.kjson.JSONObject;
import io.kjson.JSONString;
import io.kjson.JSONValue;
import io.kjson.yaml.YAML;

public final class YamlAdapter {
    private YamlAdapter() { }

    // Parse one local YAML document with YAML.parse(InputStream, UTF-8) and print the typed tree.
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("kjson-yaml")) System.exit(2);
        JSONValue root;
        try (InputStream input = Files.newInputStream(Path.of(args[1]))) {
            root = YAML.INSTANCE.parse(input, StandardCharsets.UTF_8).getRootNode();
        }
        StringBuilder out = new StringBuilder();
        tree(root, out);
        System.out.println("{\"tree\":" + out + "}");
    }

    private static void tree(JSONValue node, StringBuilder out) throws java.io.IOException {
        if (node instanceof JSONObject object) {
            out.append("[\"map\",[");
            boolean first = true;
            for (Map.Entry<String, JSONValue> entry : object.entrySet()) {
                if (!first) out.append(',');
                first = false;
                out.append('[');
                quote(entry.getKey(), out);
                out.append(',');
                tree(entry.getValue(), out);
                out.append(']');
            }
            out.append("]]");
        } else if (node instanceof JSONArray array) {
            out.append("[\"seq\",[");
            for (int index = 0; index < array.size(); index++) {
                if (index > 0) out.append(',');
                tree(array.get(index), out);
            }
            out.append("]]");
        } else if (node instanceof JSONString text) {
            out.append("[\"str\",");
            quote(text.getValue(), out);
            out.append(']');
        } else if (node instanceof JSONInt value) {
            out.append("[\"int\",\"").append(value.getValue()).append("\"]");
        } else if (node instanceof JSONLong value) {
            out.append("[\"int\",\"").append(value.getValue()).append("\"]");
        } else if (node instanceof JSONDecimal value) {
            out.append("[\"float\",\"").append(Double.toString(value.getValue().doubleValue())).append("\"]");
        } else if (node instanceof JSONBoolean value) {
            out.append("[\"bool\",").append(value.getAsBoolean()).append(']');
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
