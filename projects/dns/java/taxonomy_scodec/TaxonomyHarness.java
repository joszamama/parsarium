import fr.davit.taxonomy.model.DnsHeader;
import fr.davit.taxonomy.model.DnsMessage;
import fr.davit.taxonomy.model.DnsQuestion;
import fr.davit.taxonomy.model.record.DnsAAAARecordData;
import fr.davit.taxonomy.model.record.DnsARecordData;
import fr.davit.taxonomy.model.record.DnsCNAMERecordData;
import fr.davit.taxonomy.model.record.DnsMXRecordData;
import fr.davit.taxonomy.model.record.DnsNSRecordData;
import fr.davit.taxonomy.model.record.DnsPTRRecordData;
import fr.davit.taxonomy.model.record.DnsRecordData;
import fr.davit.taxonomy.model.record.DnsResourceRecord;
import fr.davit.taxonomy.model.record.DnsTXTRecordData;
import fr.davit.taxonomy.scodec.DnsCodec$;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Locale;
import scala.jdk.javaapi.CollectionConverters;
import scodec.DecodeResult;
import scodec.bits.BitVector$;

/** Local DNS message bytes reach taxonomy-scodec's DnsCodec.dnsMessage decoder. No fs2 socket, resolver or network is used. */
public final class TaxonomyHarness {
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

    static String rdata(DnsRecordData data) {
        // taxonomy builds A/AAAA as java.net.Inet4Address/Inet6Address from the decoded bytes (no lookup);
        // A text is getHostAddress(), AAAA text is formatted from getAddress() (RFC 5952).
        if (data instanceof DnsARecordData a) return a.address().getHostAddress();
        if (data instanceof DnsAAAARecordData aaaa) return ipv6(aaaa.address().getAddress());
        if (data instanceof DnsCNAMERecordData cname) return absolute(cname.cname());
        if (data instanceof DnsNSRecordData ns) return absolute(ns.nsdname());
        if (data instanceof DnsPTRRecordData ptr) return absolute(ptr.ptrdname());
        if (data instanceof DnsMXRecordData mx) return mx.preference() + " " + absolute(mx.exchange());
        if (data instanceof DnsTXTRecordData txt) {
            StringBuilder out = new StringBuilder();
            for (String text : CollectionConverters.asJava(txt.txt())) out.append(out.length() == 0 ? "" : " ").append(quote(text));
            return out.toString();
        }
        throw new IllegalArgumentException("record type outside the control subset: " + data);
    }

    static String records(scala.collection.Seq<DnsResourceRecord> section) {
        List<DnsResourceRecord> records = CollectionConverters.asJava(section);
        StringBuilder out = new StringBuilder("[");
        for (int i = 0; i < records.size(); i++) {
            DnsResourceRecord record = records.get(i);
            if (i > 0) out.append(',');
            // The case-class field `class` is read through productElement(2); the 1-bit mDNS cache-flush
            // flag the codec splits off the class field is false for both controls.
            if (record.cacheFlush()) throw new IllegalArgumentException("cache-flush bit outside the control subset");
            out.append("{\"name\":").append(quote(absolute(record.name())))
               .append(",\"type\":").append(code(record.data().type()))
               .append(",\"class\":").append(code(record.productElement(2)))
               .append(",\"ttl\":").append(record.ttl().toSeconds())
               .append(",\"rdata\":").append(quote(rdata(record.data()))).append('}');
        }
        return out.append(']').toString();
    }

    static String questions(scala.collection.Seq<DnsQuestion> section) {
        List<DnsQuestion> questions = CollectionConverters.asJava(section);
        StringBuilder out = new StringBuilder("[");
        for (int i = 0; i < questions.size(); i++) {
            DnsQuestion question = questions.get(i);
            if (i > 0) out.append(',');
            if (question.unicastResponse()) throw new IllegalArgumentException("unicast-response bit outside the control subset");
            // `type` and `class` are Scala keywords used as field names: productElement(1) and (3).
            out.append("{\"name\":").append(quote(absolute(question.name())))
               .append(",\"type\":").append(code(question.productElement(1)))
               .append(",\"class\":").append(code(question.productElement(3))).append('}');
        }
        return out.append(']').toString();
    }

    // Enum fields are enumeratum IntEnumEntry values; value() is the decoded wire number.
    static int code(Object entry) {
        return (Integer) ((enumeratum.values.IntEnumEntry) entry).value();
    }

    static int bit(boolean value) {
        return value ? 1 : 0;
    }

    static String parse(byte[] data) {
        if (data.length == 0 || data.length > 65535) throw new IllegalArgumentException("input outside harness limit");
        DecodeResult<DnsMessage> result = DnsCodec$.MODULE$.dnsMessage().decode(BitVector$.MODULE$.apply(data)).require();
        if (!result.remainder().isEmpty()) throw new IllegalArgumentException("trailing bytes after the message");
        DnsMessage message = result.value();
        DnsHeader header = message.header();
        return "{\"id\":" + header.id()
            + ",\"qr\":" + code(header.productElement(1))
            + ",\"opcode\":" + code(header.opCode())
            + ",\"aa\":" + bit(header.isAuthoritativeAnswer())
            + ",\"tc\":" + bit(header.isTruncated())
            + ",\"rd\":" + bit(header.isRecursionDesired())
            + ",\"ra\":" + bit(header.isRecursionAvailable())
            // taxonomy reads the three bits after RA as a lenient constant and keeps none of Z, AD and CD.
            + ",\"z\":0"
            + ",\"rcode\":" + code(header.responseCode())
            + ",\"qdcount\":" + message.questions().size()
            + ",\"ancount\":" + message.answers().size()
            + ",\"nscount\":" + message.authorities().size()
            + ",\"arcount\":" + message.additionals().size()
            + ",\"questions\":" + questions(message.questions())
            + ",\"answers\":" + records(message.answers())
            + ",\"authority\":" + records(message.authorities())
            + ",\"additional\":" + records(message.additionals()) + "}";
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
