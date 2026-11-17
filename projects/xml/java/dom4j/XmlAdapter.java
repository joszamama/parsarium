package org.parsarium;

import java.io.ByteArrayInputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.TreeSet;
import org.dom4j.Attribute;
import org.dom4j.Document;
import org.dom4j.Element;
import org.dom4j.Namespace;
import org.dom4j.Node;
import org.dom4j.io.SAXReader;

public final class XmlAdapter {
    private XmlAdapter() { }

    private static final class Summary {
        final List<String> elements = new ArrayList<>(), attributes = new ArrayList<>(),
                text = new ArrayList<>();
        final TreeSet<String> namespaces = new TreeSet<>();
        final StringBuilder run = new StringBuilder();
        int declarations, depth;

        void flush() {
            String segment = run.toString().strip();
            if (!segment.isEmpty()) text.add(segment);
            run.setLength(0);
        }
    }

    // The pinned dom4j SAXReader parses one local UTF-8 XML InputStream into a
    // dom4j Document. SAXReader obtains its SAX parser through JAXP
    // SAXParserFactory.newInstance(); no factory is configured here, so the
    // runtime default (the OpenJDK java.xml Xerces fork) tokenizes the input.
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("dom4j")) System.exit(2);
        byte[] data = Files.readAllBytes(Path.of(args[1]));
        SAXReader reader = SAXReader.createDefault();
        Document document = reader.read(new ByteArrayInputStream(data));
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
        for (Map.Entry<String, String> entry : result.entrySet()) {
            parts.add(quote(entry.getKey()) + ":" + entry.getValue());
        }
        System.out.println("{" + String.join(",", parts) + "}");
    }

    // Visits the dom4j tree in document order; text runs are split at element,
    // comment and processing-instruction boundaries like the other adapters.
    private static void walk(Element element, int level, Summary summary) {
        summary.flush();
        summary.depth = Math.max(summary.depth, level);
        summary.elements.add(clark(element.getNamespaceURI(), element.getName()));
        for (Namespace namespace : element.declaredNamespaces()) {
            summary.declarations++;
            String uri = namespace.getURI();
            if (uri != null && !uri.isEmpty()) summary.namespaces.add(uri);
        }
        List<String> own = new ArrayList<>();
        for (Attribute attribute : element.attributes()) {
            own.add(clark(attribute.getNamespaceURI(), attribute.getName()) + "=" + attribute.getValue());
        }
        Collections.sort(own);
        summary.attributes.addAll(own);
        for (Node node : element.content()) {
            switch (node.getNodeType()) {
                case Node.ELEMENT_NODE -> walk((Element) node, level + 1, summary);
                case Node.TEXT_NODE, Node.CDATA_SECTION_NODE, Node.ENTITY_REFERENCE_NODE ->
                        summary.run.append(node.getText());
                case Node.COMMENT_NODE, Node.PROCESSING_INSTRUCTION_NODE -> summary.flush();
                default -> { }
            }
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
