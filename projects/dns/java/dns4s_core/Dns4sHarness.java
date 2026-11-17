import com.github.mkroli.dns4s.Message;
import com.github.mkroli.dns4s.Message$;
import com.github.mkroli.dns4s.MessageBuffer$;
import com.github.mkroli.dns4s.section.HeaderSection;
import com.github.mkroli.dns4s.section.QuestionSection;
import com.github.mkroli.dns4s.section.ResourceRecord;
import com.github.mkroli.dns4s.section.resource.AAAAResource;
import com.github.mkroli.dns4s.section.resource.AResource;
import com.github.mkroli.dns4s.section.resource.CNameResource;
import com.github.mkroli.dns4s.section.resource.MXResource;
import com.github.mkroli.dns4s.section.resource.NSResource;
import com.github.mkroli.dns4s.section.resource.PTRResource;
import com.github.mkroli.dns4s.section.resource.TXTResource;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Locale;
import scala.jdk.javaapi.CollectionConverters;

/** Local DNS message bytes reach dns4s-core's Message.apply(MessageBuffer) decoder. No Akka, Netty or socket is used. */
public final class Dns4sHarness {
    static String absolute(String name) {
        String lower = name.toLowerCase(Locale.ROOT);
        return lower.endsWith(".") ? lower : lower + ".";
    }

    // RFC 5952 text from the 16 decoded address bytes.
    static String ipv6(byte[] bytes) {
        int[] groups = new int[8];
        for (int i = 0; i < 8; i++) groups[i] = ((bytes[2 * i] & 0xff) << 8) | (bytes[2 * i + 1] & 0xff);
        int bestStart = -1, bestLength = 0;
        for (int i = 0; i < 8; ) {
            if (groups[i] != 0) { i++; continue; }
            int j = i;
            while (j < 8 && groups[j] == 0) j++;
            if (j - i > bestLength && j - i >= 2) { bestStart = i; bestLength = j - i; }
            i = j;
        }
        StringBuilder text = new StringBuilder();
        for (int i = 0; i < 8; i++) {
            if (i == bestStart) { text.append(i == 0 ? "::" : ":"); i += bestLength - 1; continue; }
            text.append(Integer.toHexString(groups[i]));
            if (i < 7) text.append(':');
        }
        return text.toString();
    }

    static String quote(String value) {
        return "\"" + value.replace("\\", "\\\\").replace("\"", "\\\"") + "\"";
    }

    static String rdata(Object data) {
        // dns4s builds A/AAAA as java.net.Inet4Address/Inet6Address from the decoded bytes (no lookup);
        // A text is getHostAddress(), AAAA text is formatted from getAddress() (RFC 5952).
        if (data instanceof AResource a) return a.address().getHostAddress();
        if (data instanceof AAAAResource aaaa) return ipv6(aaaa.address().getAddress());
        if (data instanceof CNameResource cname) return absolute(cname.cname());
        if (data instanceof NSResource ns) return absolute(ns.nsdname());
        if (data instanceof PTRResource ptr) return absolute(ptr.ptrdname());
        if (data instanceof MXResource mx) return mx.preference() + " " + absolute(mx.exchange());
        if (data instanceof TXTResource txt) {
            StringBuilder out = new StringBuilder();
            for (String text : CollectionConverters.asJava(txt.txt())) out.append(out.length() == 0 ? "" : " ").append(quote(text));
            return out.toString();
        }
        throw new IllegalArgumentException("record type outside the control subset: " + data);
    }

    static String records(scala.collection.Seq<ResourceRecord> section) {
        List<ResourceRecord> records = CollectionConverters.asJava(section);
        StringBuilder out = new StringBuilder("[");
        for (int i = 0; i < records.size(); i++) {
            ResourceRecord record = records.get(i);
            if (i > 0) out.append(',');
            // The case-class fields `type` and `class` are read through productElement (1 and 2).
            out.append("{\"name\":").append(quote(absolute(record.name())))
               .append(",\"type\":").append(record.productElement(1))
               .append(",\"class\":").append(record.productElement(2))
               .append(",\"ttl\":").append(record.ttl())
               .append(",\"rdata\":").append(quote(rdata(record.rdata()))).append('}');
        }
        return out.append(']').toString();
    }

    static String questions(scala.collection.Seq<QuestionSection> section) {
        List<QuestionSection> questions = CollectionConverters.asJava(section);
        StringBuilder out = new StringBuilder("[");
        for (int i = 0; i < questions.size(); i++) {
            QuestionSection question = questions.get(i);
            if (i > 0) out.append(',');
            out.append("{\"name\":").append(quote(absolute(question.qname())))
               .append(",\"type\":").append(question.qtype())
               .append(",\"class\":").append(question.qclass()).append('}');
        }
        return out.append(']').toString();
    }

    static int bit(boolean value) {
        return value ? 1 : 0;
    }

    static String parse(byte[] data) {
        if (data.length == 0 || data.length > 65535) throw new IllegalArgumentException("input outside harness limit");
        Message message = Message$.MODULE$.apply(MessageBuffer$.MODULE$.apply(ByteBuffer.wrap(data)));
        HeaderSection header = message.header();
        return "{\"id\":" + header.id()
            + ",\"qr\":" + bit(header.qr())
            + ",\"opcode\":" + header.opcode()
            + ",\"aa\":" + bit(header.aa())
            + ",\"tc\":" + bit(header.tc())
            + ",\"rd\":" + bit(header.rd())
            + ",\"ra\":" + bit(header.ra())
            // dns4s's HeaderSection decodes neither the reserved Z bit nor AD/CD.
            + ",\"z\":0"
            + ",\"rcode\":" + header.rcode()
            + ",\"qdcount\":" + message.question().size()
            + ",\"ancount\":" + message.answer().size()
            + ",\"nscount\":" + message.authority().size()
            + ",\"arcount\":" + message.additional().size()
            + ",\"questions\":" + questions(message.question())
            + ",\"answers\":" + records(message.answer())
            + ",\"authority\":" + records(message.authority())
            + ",\"additional\":" + records(message.additional()) + "}";
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (RuntimeException ignored) { }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("one input path required");
        System.out.write((parse(Files.readAllBytes(Path.of(args[0]))) + "\n").getBytes(StandardCharsets.UTF_8));
        System.out.flush();
    }
}
