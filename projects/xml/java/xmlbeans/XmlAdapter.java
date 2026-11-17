package org.parsarium;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.TreeSet;
import javax.xml.namespace.QName;
import org.apache.xmlbeans.XmlCursor;
import org.apache.xmlbeans.XmlObject;

public final class XmlAdapter {
    private XmlAdapter() { }

    private static final class Summary {
        final List<String> elements = new ArrayList<>(), attributes = new ArrayList<>(), text = new ArrayList<>();
        final List<String> ownAttributes = new ArrayList<>();
        final TreeSet<String> namespaces = new TreeSet<>();
        final StringBuilder run = new StringBuilder();
        int declarations, depth, level;

        void flushText() {
            String segment = run.toString().strip();
            if (!segment.isEmpty()) text.add(segment);
            run.setLength(0);
        }
        void flushAttributes() {
            Collections.sort(ownAttributes);
            attributes.addAll(ownAttributes);
            ownAttributes.clear();
        }
    }

    // XMLBeans builds its own cursor tree from a JAXP SAX reader (the JDK
    // Xerces fork in the pinned runtime). Report the parsed XML infoset,
    // not a serializer round trip or a regex over the original text.
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("xmlbeans")) System.exit(2);
        XmlObject document;
        try (java.io.InputStream input = Files.newInputStream(Path.of(args[1]))) {
            document = XmlObject.Factory.parse(input);
        }
        Summary summary = new Summary();
        try (XmlCursor cursor = document.newCursor()) {
            do {
                XmlCursor.TokenType token = cursor.currentTokenType();
                if (token.isAttr()) {
                    summary.ownAttributes.add(clark(cursor.getName()) + "=" + cursor.getTextValue());
                } else if (token.isNamespace()) {
                    summary.declarations++;
                    String uri = cursor.getTextValue();
                    if (!uri.isEmpty()) summary.namespaces.add(uri);
                } else {
                    summary.flushAttributes();
                    if (token.isText()) {
                        summary.run.append(cursor.getTextValue());
                    } else {
                        summary.flushText();
                        if (token.isStart()) {
                            summary.elements.add(clark(cursor.getName()));
                            summary.level++;
                            summary.depth = Math.max(summary.depth, summary.level);
                        } else if (token.isEnd()) {
                            summary.level--;
                        }
                    }
                }
            } while (cursor.toNextToken() != XmlCursor.TokenType.NONE);
        }
        summary.flushText();
        summary.flushAttributes();
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

    private static String clark(QName name) {
        String space = name.getNamespaceURI();
        return space == null || space.isEmpty() ? name.getLocalPart() : "{" + space + "}" + name.getLocalPart();
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
