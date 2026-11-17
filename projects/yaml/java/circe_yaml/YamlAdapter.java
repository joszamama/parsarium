package org.parsarium;

import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import io.circe.Json;
import io.circe.JsonNumber;
import io.circe.ParsingFailure;
import scala.Tuple2;
import scala.collection.Iterator;
import scala.util.Either;

public final class YamlAdapter {
    private YamlAdapter() { }

    // Parse one local YAML document with io.circe.yaml.parser.parse(Reader) and print the typed tree.
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("circe-yaml")) System.exit(2);
        Either<ParsingFailure, Json> parsed;
        try (Reader input = Files.newBufferedReader(Path.of(args[1]), StandardCharsets.UTF_8)) {
            parsed = io.circe.yaml.parser.package$.MODULE$.parse(input);
        }
        if (parsed.isLeft()) throw parsed.left().get();
        StringBuilder out = new StringBuilder();
        tree(parsed.right().get(), out);
        System.out.println("{\"tree\":" + out + "}");
    }

    // circe Json numbers keep no int/float type: a number with an exact Long value is typed int
    // (the controls contain no integral-valued floats), any other number is a float.
    private static void tree(Json node, StringBuilder out) throws java.io.IOException {
        if (node.isObject()) {
            out.append("[\"map\",[");
            Iterator<Tuple2<String, Json>> entries = node.asObject().get().toIterable().iterator();
            boolean first = true;
            while (entries.hasNext()) {
                Tuple2<String, Json> entry = entries.next();
                if (!first) out.append(',');
                first = false;
                out.append('[');
                quote(entry._1(), out);
                out.append(',');
                tree(entry._2(), out);
                out.append(']');
            }
            out.append("]]");
        } else if (node.isArray()) {
            out.append("[\"seq\",[");
            Iterator<Json> items = node.asArray().get().iterator();
            boolean first = true;
            while (items.hasNext()) {
                if (!first) out.append(',');
                first = false;
                tree(items.next(), out);
            }
            out.append("]]");
        } else if (node.isString()) {
            out.append("[\"str\",");
            quote(node.asString().get(), out);
            out.append(']');
        } else if (node.isNumber()) {
            JsonNumber number = node.asNumber().get();
            if (number.toLong().isDefined()) {
                out.append("[\"int\",\"").append(number.toLong().get()).append("\"]");
            } else {
                double value = number.toDouble();
                if (Double.isNaN(value) || Double.isInfinite(value)) throw new java.io.IOException("non-finite number");
                out.append("[\"float\",\"").append(Double.toString(value)).append("\"]");
            }
        } else if (node.isBoolean()) {
            out.append("[\"bool\",").append(node.asBoolean().get()).append(']');
        } else if (node.isNull()) {
            out.append("[\"null\"]");
        } else {
            throw new java.io.IOException("unexpected JSON value");
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
