package org.parsarium;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.TreeSet;
import org.xmlpull.mxp1.MXParser;
import org.xmlpull.v1.XmlPullParser;

public final class XmlAdapter {
    private XmlAdapter() { }

    private static final class Summary {
        final List<String> elements = new ArrayList<>(), attributes = new ArrayList<>(), text = new ArrayList<>();
        final TreeSet<String> namespaces = new TreeSet<>();
        final StringBuilder run = new StringBuilder();
        int declarations, depth;
        void flush() {
            String segment = run.toString().strip();
            if (!segment.isEmpty()) text.add(segment);
            run.setLength(0);
        }
    }

    // MXParser tokenizes the local byte stream; next() resolves text references.
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("xpp3")) System.exit(2);
        XmlPullParser parser = new MXParser();
        parser.setFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES, true);
        Summary summary = new Summary();
        try (java.io.InputStream input = Files.newInputStream(Path.of(args[1]))) {
            parser.setInput(input, null);
            while (true) {
                int event = parser.next();
                if (event == XmlPullParser.END_DOCUMENT) break;
                if (event == XmlPullParser.START_TAG) {
                    summary.flush();
                    int depth = parser.getDepth();
                    summary.depth = Math.max(summary.depth, depth);
                    summary.elements.add(clark(parser.getNamespace(), parser.getName()));
                    for (int i = parser.getNamespaceCount(depth - 1);
                            i < parser.getNamespaceCount(depth); i++) {
                        summary.declarations++;
                        String uri = parser.getNamespaceUri(i);
                        if (uri != null && !uri.isEmpty()) summary.namespaces.add(uri);
                    }
                    List<String> own = new ArrayList<>();
                    for (int i = 0; i < parser.getAttributeCount(); i++) {
                        own.add(clark(parser.getAttributeNamespace(i), parser.getAttributeName(i))
                                + "=" + parser.getAttributeValue(i));
                    }
                    Collections.sort(own);
                    summary.attributes.addAll(own);
                } else if (event == XmlPullParser.END_TAG) {
                    summary.flush();
                } else if (event == XmlPullParser.TEXT) {
                    summary.run.append(parser.getText());
                }
            }
        }
        summary.flush();
        Map<String, String> result = new TreeMap<>();
        result.put("attributes", list(summary.attributes));
        result.put("elements", list(summary.elements));
        result.put("max_depth", Integer.toString(summary.depth));
        result.put("namespace_declarations", Integer.toString(summary.declarations));
        result.put("namespaces", list(new ArrayList<>(summary.namespaces)));
        result.put("root", quote(summary.elements.get(0)));
        result.put("text", list(summary.text));
        List<String> parts = new ArrayList<>();
        for (Map.Entry<String, String> entry : result.entrySet())
            parts.add(quote(entry.getKey()) + ":" + entry.getValue());
        System.out.println("{" + String.join(",", parts) + "}");
    }

    private static String clark(String space, String local) {
        return space == null || space.isEmpty() ? local : "{" + space + "}" + local;
    }
    private static String list(List<String> values) {
        List<String> quoted = new ArrayList<>();
        for (String value : values) quoted.add(quote(value));
        return "[" + String.join(",", quoted) + "]";
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
