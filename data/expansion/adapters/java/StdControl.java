// JDK java.xml and Java Sound control adapter. Usage: java StdControl.java <api> <control>
import java.io.*;
import java.nio.file.*;
import java.util.*;
import javax.xml.parsers.*;
import javax.xml.stream.*;
import org.w3c.dom.*;

public class StdControl {
  static String q(String s) { return "\"" + s.replace("\\", "\\\\").replace("\"", "\\\"") + "\""; }
  static String list(List<String> l) { List<String> o = new ArrayList<>(); for (String s : l) o.add(q(s)); return "[" + String.join(", ", o) + "]"; }

  public static void main(String[] a) throws Exception {
    byte[] data = Files.readAllBytes(Path.of(a[1]));
    String root = null; int children = 0; List<String> ids = new ArrayList<>(), texts = new ArrayList<>();
    switch (a[0]) {
      case "javax.xml.parsers.DocumentBuilder.parse" -> {
        DocumentBuilderFactory f = DocumentBuilderFactory.newInstance(); f.setNamespaceAware(true);
        Element r = f.newDocumentBuilder().parse(new ByteArrayInputStream(data)).getDocumentElement();
        root = "{" + r.getNamespaceURI() + "}" + r.getLocalName();
        for (Node n = r.getFirstChild(); n != null; n = n.getNextSibling()) {
          if (n.getNodeType() != Node.ELEMENT_NODE) continue;
          children++;
          if (n.getLocalName().equals("item")) { ids.add(((Element) n).getAttribute("id")); texts.add(n.getTextContent()); }
        }
      }
      case "javax.xml.stream.XMLStreamReader" -> {
        XMLStreamReader x = XMLInputFactory.newFactory().createXMLStreamReader(new ByteArrayInputStream(data));
        int depth = 0; StringBuilder cur = null;
        while (x.hasNext()) {
          int ev = x.next();
          if (ev == XMLStreamConstants.START_ELEMENT) {
            depth++;
            if (depth == 1) root = "{" + x.getNamespaceURI() + "}" + x.getLocalName();
            else if (depth == 2) { children++; if (x.getLocalName().equals("item")) { ids.add(x.getAttributeValue(null, "id")); cur = new StringBuilder(); } }
          } else if ((ev == XMLStreamConstants.CHARACTERS || ev == XMLStreamConstants.CDATA) && cur != null) cur.append(x.getText());
          else if (ev == XMLStreamConstants.END_ELEMENT) { if (depth == 2 && cur != null) { texts.add(cur.toString()); cur = null; } depth--; }
        }
      }
      case "javax.sound.sampled.AudioSystem.getAudioFileFormat" -> {
        try {
          var fmt = javax.sound.sampled.AudioSystem.getAudioFileFormat(new BufferedInputStream(new ByteArrayInputStream(data)));
          System.out.println("{\"accepted\": true, \"type\": " + q(fmt.getType().toString()) + "}");
        } catch (javax.sound.sampled.UnsupportedAudioFileException e) {
          System.out.println("{\"accepted\": false, \"exception\": \"UnsupportedAudioFileException\"}");
        }
        return;
      }
      default -> throw new IllegalArgumentException(a[0]);
    }
    System.out.println("{\"children\": " + children + ", \"ids\": " + list(ids) + ", \"root\": " + q(root) + ", \"texts\": " + list(texts) + "}");
  }
}
