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
import org.w3c.dom.Attr;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
import org.xml.sax.InputSource;

public final class XmlAdapter {
    private XmlAdapter() { }

    private static final String XMLNS = "http://www.w3.org/2000/xmlns/";

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

    // Parses one XML document from an in-memory byte stream with Apache Xerces2-J's
    // native org.apache.xerces.parsers.DOMParser, namespace processing on, and prints a
    // structural summary encoded without a JSON library.
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("xercesImpl")) System.exit(2);
        byte[] data = Files.readAllBytes(Path.of(args[1]));
        org.apache.xerces.parsers.DOMParser parser = new org.apache.xerces.parsers.DOMParser();
        parser.setFeature("http://xml.org/sax/features/namespaces", true);
        parser.parse(new InputSource(new ByteArrayInputStream(data)));
        Document document = parser.getDocument();
        Summary summary = new Summary();
        walk(document.getDocumentElement(), 1, summary);
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

    private static void walk(Element element, int level, Summary summary) {
        summary.flush();
        summary.depth = Math.max(summary.depth, level);
        summary.elements.add(clark(element.getNamespaceURI(), element.getLocalName()));
        // DOM attribute maps carry no document order, so each element's
        // attributes are listed sorted by Clark name.
        NamedNodeMap attributes = element.getAttributes();
        List<String> own = new ArrayList<>();
        for (int index = 0; index < attributes.getLength(); index++) {
            Attr attribute = (Attr) attributes.item(index);
            if (XMLNS.equals(attribute.getNamespaceURI())) {
                summary.declarations++;
                if (!attribute.getValue().isEmpty()) summary.namespaces.add(attribute.getValue());
                continue;
            }
            own.add(clark(attribute.getNamespaceURI(), attribute.getLocalName())
                    + "=" + attribute.getValue());
        }
        Collections.sort(own);
        summary.attributes.addAll(own);
        for (Node child = element.getFirstChild(); child != null; child = child.getNextSibling()) {
            switch (child.getNodeType()) {
                case Node.ELEMENT_NODE -> walk((Element) child, level + 1, summary);
                case Node.TEXT_NODE, Node.CDATA_SECTION_NODE -> summary.run.append(child.getNodeValue());
                default -> summary.flush();
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
