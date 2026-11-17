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
import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamConstants;
import javax.xml.stream.XMLStreamReader;
import com.fasterxml.aalto.stax.InputFactoryImpl;

public final class XmlAdapter {
    private XmlAdapter() { }

    private static final class Summary {
        final List<String> elements = new ArrayList<>(), attributes = new ArrayList<>(),
                text = new ArrayList<>();
        final TreeSet<String> namespaces = new TreeSet<>();
        final StringBuilder run = new StringBuilder();
        int declarations, depth, level;

        void flush() {
            String segment = run.toString().strip();
            if (!segment.isEmpty()) text.add(segment);
            run.setLength(0);
        }
    }

    // The pinned Aalto implementation parses one local UTF-8 XML InputStream.
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("aalto-xml")) System.exit(2);
        byte[] data = Files.readAllBytes(Path.of(args[1]));
        InputFactoryImpl factory = new InputFactoryImpl();
        factory.setProperty(XMLInputFactory.IS_NAMESPACE_AWARE, Boolean.TRUE);
        factory.setProperty(XMLInputFactory.SUPPORT_DTD, Boolean.FALSE);
        factory.setProperty(XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES, Boolean.FALSE);
        factory.setProperty(XMLInputFactory.IS_REPLACING_ENTITY_REFERENCES, Boolean.TRUE);
        Summary summary = new Summary();
        XMLStreamReader reader = factory.createXMLStreamReader(new ByteArrayInputStream(data));
        try {
            while (reader.hasNext()) {
                int event = reader.next();
                switch (event) {
                    case XMLStreamConstants.START_ELEMENT -> {
                        summary.flush();
                        summary.level++;
                        summary.depth = Math.max(summary.depth, summary.level);
                        summary.elements.add(clark(reader.getNamespaceURI(), reader.getLocalName()));
                        for (int i = 0; i < reader.getNamespaceCount(); i++) {
                            summary.declarations++;
                            String uri = reader.getNamespaceURI(i);
                            if (uri != null && !uri.isEmpty()) summary.namespaces.add(uri);
                        }
                        List<String> own = new ArrayList<>();
                        for (int i = 0; i < reader.getAttributeCount(); i++) {
                            own.add(clark(reader.getAttributeNamespace(i), reader.getAttributeLocalName(i))
                                    + "=" + reader.getAttributeValue(i));
                        }
                        Collections.sort(own);
                        summary.attributes.addAll(own);
                    }
                    case XMLStreamConstants.END_ELEMENT -> {
                        summary.flush();
                        summary.level--;
                    }
                    case XMLStreamConstants.CHARACTERS, XMLStreamConstants.CDATA,
                         XMLStreamConstants.SPACE, XMLStreamConstants.ENTITY_REFERENCE ->
                            summary.run.append(reader.getText());
                    case XMLStreamConstants.COMMENT, XMLStreamConstants.PROCESSING_INSTRUCTION ->
                            summary.flush();
                    default -> { }
                }
            }
            summary.flush();
        } finally {
            reader.close();
        }
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
