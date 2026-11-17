import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Locale;
import org.minidns.dnsmessage.DnsMessage;
import org.minidns.dnsmessage.Question;
import org.minidns.dnsname.DnsName;
import org.minidns.record.A;
import org.minidns.record.AAAA;
import org.minidns.record.CNAME;
import org.minidns.record.Data;
import org.minidns.record.MX;
import org.minidns.record.NS;
import org.minidns.record.PTR;
import org.minidns.record.Record;
import org.minidns.record.TXT;

/** Local DNS message bytes reach MiniDNS's documented DnsMessage(byte[]) constructor. No resolver or client is used. */
public final class MiniDnsHarness {
    static String absolute(DnsName name) {
        String lower = name.ace.toLowerCase(Locale.ROOT);
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

    static String rdata(Data data) {
        if (data instanceof A a) return a.toString();  // MiniDNS's own dotted quad
        if (data instanceof AAAA aaaa) return ipv6(aaaa.getIp());
        if (data instanceof CNAME cname) return absolute(cname.target);
        if (data instanceof NS ns) return absolute(ns.target);
        if (data instanceof PTR ptr) return absolute(ptr.target);
        if (data instanceof MX mx) return mx.priority + " " + absolute(mx.target);
        if (data instanceof TXT txt) {
            StringBuilder out = new StringBuilder();
            for (String text : txt.getCharacterStrings()) out.append(out.length() == 0 ? "" : " ").append(quote(text));
            return out.toString();
        }
        return String.valueOf(data);
    }

    static String records(List<Record<? extends Data>> records) {
        StringBuilder out = new StringBuilder("[");
        for (int i = 0; i < records.size(); i++) {
            Record<? extends Data> record = records.get(i);
            if (i > 0) out.append(',');
            out.append("{\"name\":").append(quote(absolute(record.name)))
               .append(",\"type\":").append(record.typeValue)
               .append(",\"class\":").append(record.clazzValue)
               .append(",\"ttl\":").append(record.ttl)
               .append(",\"rdata\":").append(quote(rdata(record.payloadData))).append('}');
        }
        return out.append(']').toString();
    }

    static String questions(List<Question> questions) {
        StringBuilder out = new StringBuilder("[");
        for (int i = 0; i < questions.size(); i++) {
            Question question = questions.get(i);
            if (i > 0) out.append(',');
            out.append("{\"name\":").append(quote(absolute(question.name)))
               .append(",\"type\":").append(question.typeValue)
               .append(",\"class\":").append(question.clazz.getValue()).append('}');
        }
        return out.append(']').toString();
    }

    static int bit(boolean value) {
        return value ? 1 : 0;
    }

    static String parse(byte[] data) throws IOException {
        if (data.length == 0 || data.length > 65535) throw new IllegalArgumentException("input outside harness limit");
        DnsMessage message = new DnsMessage(data);
        return "{\"id\":" + message.id
            + ",\"qr\":" + bit(message.qr)
            + ",\"opcode\":" + message.opcode.getValue()
            + ",\"aa\":" + bit(message.authoritativeAnswer)
            + ",\"tc\":" + bit(message.truncated)
            + ",\"rd\":" + bit(message.recursionDesired)
            + ",\"ra\":" + bit(message.recursionAvailable)
            // MiniDNS decodes AD and CD but not the reserved Z bit.
            + ",\"z\":" + ((bit(message.authenticData) << 1) | bit(message.checkingDisabled))
            + ",\"rcode\":" + message.responseCode.getValue()
            + ",\"qdcount\":" + message.questions.size()
            + ",\"ancount\":" + message.answerSection.size()
            + ",\"nscount\":" + message.authoritySection.size()
            + ",\"arcount\":" + message.additionalSection.size()
            + ",\"questions\":" + questions(message.questions)
            + ",\"answers\":" + records(message.answerSection)
            + ",\"authority\":" + records(message.authoritySection)
            + ",\"additional\":" + records(message.additionalSection) + "}";
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (IOException | IllegalArgumentException | IllegalStateException ignored) { }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("one input path required");
        System.out.write((parse(Files.readAllBytes(Path.of(args[0]))) + "\n").getBytes(StandardCharsets.UTF_8));
        System.out.flush();
    }
}
