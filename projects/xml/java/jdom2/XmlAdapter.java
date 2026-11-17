package org.parsarium;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.TreeSet;
import org.jdom2.Attribute;
import org.jdom2.Content;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.Namespace;
import org.jdom2.Text;
import org.jdom2.input.SAXBuilder;

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

    // JDOM SAXBuilder builds a format-aware tree from local stream bytes.
    // Its default JAXP XMLReader is the pinned runtime's Xerces fork.
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("jdom2")) System.exit(2);
        Document document;
        try (java.io.InputStream input = Files.newInputStream(Path.of(args[1]))) {
            document = new SAXBuilder().build(input);
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
        summary.elements.add(clark(element.getNamespaceURI(), element.getName()));
        for (Namespace namespace : element.getNamespacesIntroduced()) {
            summary.declarations++;
            String uri = namespace.getURI();
            if (uri != null && !uri.isEmpty()) summary.namespaces.add(uri);
        }
        List<String> own = new ArrayList<>();
        for (Attribute attribute : element.getAttributes())
            own.add(clark(attribute.getNamespaceURI(), attribute.getName()) + "=" + attribute.getValue());
        Collections.sort(own);
        summary.attributes.addAll(own);
        for (Content content : element.getContent()) {
            if (content instanceof Element child) walk(child, level + 1, summary);
            else if (content instanceof Text text) summary.run.append(text.getText());
            else if (content instanceof org.jdom2.EntityRef ref) summary.run.append(ref.getValue());
            else if (content instanceof org.jdom2.Comment || content instanceof org.jdom2.ProcessingInstruction)
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
