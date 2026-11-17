import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Locale;
import org.pcap4j.packet.DnsDomainName;
import org.pcap4j.packet.DnsPacket;
import org.pcap4j.packet.DnsPacket.DnsHeader;
import org.pcap4j.packet.DnsQuestion;
import org.pcap4j.packet.DnsRDataA;
import org.pcap4j.packet.DnsRDataAaaa;
import org.pcap4j.packet.DnsRDataCName;
import org.pcap4j.packet.DnsRDataMx;
import org.pcap4j.packet.DnsRDataNs;
import org.pcap4j.packet.DnsRDataPtr;
import org.pcap4j.packet.DnsRDataTxt;
import org.pcap4j.packet.DnsResourceRecord;
import org.pcap4j.packet.IllegalRawDataException;

/**
 * Local DNS message bytes reach Pcap4J's documented DnsPacket.newPacket(byte[], int, int). No capture
 * handle, network interface or libpcap call is used; names are decompressed with the documented
 * DnsDomainName.decompress(headerRawData) against the same message bytes.
 */
public final class Pcap4jDnsHarness {
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

    // DnsDomainName.decompress joins the in-place labels and the pointed-to name with "."; for a name
    // that is only a compression pointer the in-place part is empty, so Pcap4J returns a leading ".".
    // The harness drops that one empty leading label; the labels themselves come from Pcap4J.
    static String name(DnsDomainName name, byte[] message) throws IllegalRawDataException {
        String text = name.decompress(message);
        if (text.length() > 1 && text.startsWith(".") && name.getLabels().isEmpty()) text = text.substring(1);
        return absolute(text);
    }

    static String rdata(DnsResourceRecord record, byte[] message) throws IllegalRawDataException {
        Object data = record.getRData();
        if (data instanceof DnsRDataA a) return a.getAddress().getHostAddress();
        if (data instanceof DnsRDataAaaa aaaa) return ipv6(aaaa.getAddress().getAddress());
        if (data instanceof DnsRDataCName cname) return name(cname.getCName(), message);
        if (data instanceof DnsRDataNs ns) return name(ns.getNsDName(), message);
        if (data instanceof DnsRDataPtr ptr) return name(ptr.getPtrDName(), message);
        if (data instanceof DnsRDataMx mx) return mx.getPreferenceAsInt() + " " + name(mx.getExchange(), message);
        if (data instanceof DnsRDataTxt txt) {
            StringBuilder out = new StringBuilder();
            for (String text : txt.getTexts()) out.append(out.length() == 0 ? "" : " ").append(quote(text));
            return out.toString();
        }
        return String.valueOf(data);
    }

    static String records(List<DnsResourceRecord> records, byte[] message) throws IllegalRawDataException {
        StringBuilder out = new StringBuilder("[");
        for (int i = 0; i < records.size(); i++) {
            DnsResourceRecord record = records.get(i);
            if (i > 0) out.append(',');
            out.append("{\"name\":").append(quote(name(record.getName(), message)))
               .append(",\"type\":").append(record.getDataType().value() & 0xffff)
               .append(",\"class\":").append(record.getDataClass().value() & 0xffff)
               .append(",\"ttl\":").append(record.getTtlAsLong())
               .append(",\"rdata\":").append(quote(rdata(record, message))).append('}');
        }
        return out.append(']').toString();
    }

    static String questions(List<DnsQuestion> questions, byte[] message) throws IllegalRawDataException {
        StringBuilder out = new StringBuilder("[");
        for (int i = 0; i < questions.size(); i++) {
            DnsQuestion question = questions.get(i);
            if (i > 0) out.append(',');
            out.append("{\"name\":").append(quote(name(question.getQName(), message)))
               .append(",\"type\":").append(question.getQType().value() & 0xffff)
               .append(",\"class\":").append(question.getQClass().value() & 0xffff).append('}');
        }
        return out.append(']').toString();
    }

    static int bit(boolean value) {
        return value ? 1 : 0;
    }

    static String parse(byte[] data) throws IllegalRawDataException {
        if (data.length == 0 || data.length > 65535) throw new IllegalArgumentException("input outside harness limit");
        DnsPacket packet = DnsPacket.newPacket(data, 0, data.length);
        DnsHeader header = packet.getHeader();
        return "{\"id\":" + (header.getId() & 0xffff)
            + ",\"qr\":" + bit(header.isResponse())
            + ",\"opcode\":" + header.getOpCode().value()
            + ",\"aa\":" + bit(header.isAuthoritativeAnswer())
            + ",\"tc\":" + bit(header.isTruncated())
            + ",\"rd\":" + bit(header.isRecursionDesired())
            + ",\"ra\":" + bit(header.isRecursionAvailable())
            + ",\"z\":" + ((bit(header.getReservedBit()) << 2) | (bit(header.isAuthenticData()) << 1)
                           | bit(header.isCheckingDisabled()))
            + ",\"rcode\":" + header.getrCode().value()
            + ",\"qdcount\":" + header.getQdCountAsInt()
            + ",\"ancount\":" + header.getAnCountAsInt()
            + ",\"nscount\":" + header.getNsCountAsInt()
            + ",\"arcount\":" + header.getArCountAsInt()
            + ",\"questions\":" + questions(header.getQuestions(), data)
            + ",\"answers\":" + records(header.getAnswers(), data)
            + ",\"authority\":" + records(header.getAuthorities(), data)
            + ",\"additional\":" + records(header.getAdditionalInfo(), data) + "}";
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (IllegalRawDataException | IllegalArgumentException ignored) { }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("one input path required");
        System.out.write((parse(Files.readAllBytes(Path.of(args[0]))) + "\n").getBytes(StandardCharsets.UTF_8));
        System.out.flush();
    }
}
