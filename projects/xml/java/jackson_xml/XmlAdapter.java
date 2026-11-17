package org.parsarium;

import com.ctc.wstx.stax.WstxInputFactory;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonToken;
import com.fasterxml.jackson.dataformat.xml.XmlFactory;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import javax.xml.stream.XMLInputFactory;

public final class XmlAdapter {
    private XmlAdapter() { }

    // XmlFactory creates a FromXmlParser over a pinned Woodstox StAX reader.
    // Jackson's XML-to-JSON token projection drops namespace URIs, root name,
    // comments and processing instructions; the ordered token stream is the
    // observable API result, rather than a claim to preserve the full XML tree.
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("jackson-dataformat-xml")) System.exit(2);
        WstxInputFactory stax = new WstxInputFactory();
        stax.setProperty(XMLInputFactory.IS_NAMESPACE_AWARE, Boolean.TRUE);
        stax.setProperty(XMLInputFactory.SUPPORT_DTD, Boolean.FALSE);
        stax.setProperty(XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES, Boolean.FALSE);
        XmlFactory factory = new XmlFactory(stax);
        List<String> events = new ArrayList<>();
        try (java.io.InputStream input = Files.newInputStream(Path.of(args[1]));
             JsonParser parser = factory.createParser(input)) {
            for (JsonToken token = parser.nextToken(); token != null; token = parser.nextToken()) {
                String event = token.name();
                if (token == JsonToken.FIELD_NAME || token == JsonToken.VALUE_STRING)
                    event += ":" + parser.getText();
                events.add(event);
            }
        }
        List<String> quoted = new ArrayList<>();
        for (String event : events) quoted.add(quote(event));
        System.out.println("{\"events\":[" + String.join(",", quoted)
                + "],\"token_count\":" + events.size() + "}");
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
