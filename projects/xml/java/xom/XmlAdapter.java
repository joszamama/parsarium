package org.parsarium;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.TreeSet;
import nu.xom.Attribute;
import nu.xom.Builder;
import nu.xom.Document;
import nu.xom.Element;
import nu.xom.Node;
import nu.xom.Text;

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

    // XOM builds a tree from a local stream through its selected SAX reader.
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("xom")) System.exit(2);
        Document document;
        try (java.io.InputStream input = Files.newInputStream(Path.of(args[1]))) {
            document = new Builder().build(input);
        }
        Summary summary = new Summary();
        walk(document.getRootElement(), 1, summary);
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

    private static void walk(Element element, int level, Summary summary) {
        summary.flush();
        summary.depth = Math.max(summary.depth, level);
        summary.elements.add(clark(element.getNamespaceURI(), element.getLocalName()));
        for (int i = 0; i < element.getNamespaceDeclarationCount(); i++) {
            String prefix = element.getNamespacePrefix(i);
            String uri = element.getNamespaceURI(prefix);
            if (element.getParent() instanceof Element parent &&
                    uri.equals(parent.getNamespaceURI(prefix))) continue;
            summary.declarations++;
            if (uri != null && !uri.isEmpty()) summary.namespaces.add(uri);
        }
        List<String> own = new ArrayList<>();
        for (int i = 0; i < element.getAttributeCount(); i++) {
            Attribute attribute = element.getAttribute(i);
            own.add(clark(attribute.getNamespaceURI(), attribute.getLocalName()) + "=" + attribute.getValue());
        }
        Collections.sort(own);
        summary.attributes.addAll(own);
        for (int i = 0; i < element.getChildCount(); i++) {
            Node child = element.getChild(i);
            if (child instanceof Element nested) walk(nested, level + 1, summary);
            else if (child instanceof Text text) summary.run.append(text.getValue());
            else if (child instanceof nu.xom.Comment || child instanceof nu.xom.ProcessingInstruction)
                summary.flush();
        }
        summary.flush();
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
