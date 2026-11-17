package org.parsarium;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import scala.Tuple2;
import scala.collection.Iterator;
import scala.util.Either;
import zio.json.JsonDecoder;
import zio.json.ast.Json;

public final class YamlAdapter {
    private YamlAdapter() { }

    // Parse one local YAML document with the documented String#fromYaml[Json] extension of
    // zio.json.yaml._ and print the typed tree. Scala compiles the extension to
    // package$DecoderYamlOps$.fromYaml$extension(String, JsonDecoder); Java cannot name the
    // Scala package object `package`, so the compiled method is looked up once by name.
    private static final Method FROM_YAML;
    private static final Object OPS;

    static {
        try {
            Class<?> ops = Class.forName("zio.json.yaml.package$DecoderYamlOps$");
            FROM_YAML = ops.getMethod("fromYaml$extension", String.class, JsonDecoder.class);
            OPS = ops.getField("MODULE$").get(null);
        } catch (ReflectiveOperationException error) {
            throw new ExceptionInInitializerError(error);
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("zio-json-yaml")) System.exit(2);
        String yaml = Files.readString(Path.of(args[1]), StandardCharsets.UTF_8);
        Either<String, Json> parsed;
        try {
            @SuppressWarnings("unchecked")
            Either<String, Json> result = (Either<String, Json>) FROM_YAML.invoke(OPS, yaml, zio.json.ast.Json$.MODULE$.decoder());
            parsed = result;
        } catch (InvocationTargetException error) {
            Throwable cause = error.getCause();
            if (cause instanceof Exception checked) throw checked;
            if (cause instanceof Error failure) throw failure;
            throw error;
        }
        if (parsed.isLeft()) throw new java.io.IOException(parsed.left().get());
        StringBuilder out = new StringBuilder();
        tree(parsed.right().get(), out);
        System.out.println("{\"tree\":" + out + "}");
    }

    // zio-json Json.Num holds a BigDecimal without the YAML int/float tag: a number with an exact
    // Long value is typed int (the controls contain no integral-valued floats), any other a float.
    private static void tree(Json node, StringBuilder out) throws java.io.IOException {
        if (node instanceof Json.Obj object) {
            out.append("[\"map\",[");
            Iterator<Tuple2<String, Json>> entries = object.fields().iterator();
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
        } else if (node instanceof Json.Arr array) {
            out.append("[\"seq\",[");
            Iterator<Json> items = array.elements().iterator();
            boolean first = true;
            while (items.hasNext()) {
                if (!first) out.append(',');
                first = false;
                tree(items.next(), out);
            }
            out.append("]]");
        } else if (node instanceof Json.Str text) {
            out.append("[\"str\",");
            quote(text.value(), out);
            out.append(']');
        } else if (node instanceof Json.Num number) {
            BigDecimal value = number.value();
            long exact;
            try {
                exact = value.longValueExact();
            } catch (ArithmeticException notIntegral) {
                double real = value.doubleValue();
                if (Double.isNaN(real) || Double.isInfinite(real)) throw new java.io.IOException("non-finite number");
                out.append("[\"float\",\"").append(Double.toString(real)).append("\"]");
                return;
            }
            out.append("[\"int\",\"").append(exact).append("\"]");
        } else if (node instanceof Json.Bool bool) {
            out.append("[\"bool\",").append(bool.value()).append(']');
        } else if (node == Json.Null$.MODULE$) {
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
