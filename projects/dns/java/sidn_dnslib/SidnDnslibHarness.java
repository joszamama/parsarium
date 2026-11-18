import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import nl.sidnlabs.dnslib.exception.DnsDecodeException;
import nl.sidnlabs.dnslib.message.Header;
import nl.sidnlabs.dnslib.message.Message;
import nl.sidnlabs.dnslib.message.Question;
import nl.sidnlabs.dnslib.message.RRset;
import nl.sidnlabs.dnslib.message.records.AAAAResourceRecord;
import nl.sidnlabs.dnslib.message.records.AResourceRecord;
import nl.sidnlabs.dnslib.message.records.AbstractResourceRecord;
import nl.sidnlabs.dnslib.message.records.CNAMEResourceRecord;
import nl.sidnlabs.dnslib.message.records.MXResourceRecord;
import nl.sidnlabs.dnslib.message.records.NSResourceRecord;
import nl.sidnlabs.dnslib.message.records.PTRResourceRecord;
import nl.sidnlabs.dnslib.message.records.ResourceRecord;
import nl.sidnlabs.dnslib.message.util.NetworkData;
import nl.sidnlabs.dnslib.types.MessageType;

/**
 * Local DNS message bytes reach SIDN dnslib's documented Message(NetworkData) constructor
 * ("Decode network bytes into a DNS Message"). No resolver, socket or capture is used.
 */
public final class SidnDnslibHarness {
    static String absolute(String name) {
        String lower = name.toLowerCase(Locale.ROOT);
        return lower.endsWith(".") ? lower : lower + ".";
    }

    static String quote(String value) {
        return "\"" + value.replace("\\", "\\\\").replace("\"", "\\\"") + "\"";
    }

    static String rdata(ResourceRecord record) {
        if (record instanceof AResourceRecord a) return a.getAddress();
        if (record instanceof AAAAResourceRecord aaaa) return aaaa.getAddress();  // dnslib's own RFC 5952 text
        if (record instanceof CNAMEResourceRecord cname) return absolute(cname.getCname());
        if (record instanceof NSResourceRecord ns) return absolute(ns.getNameserver());
        if (record instanceof PTRResourceRecord ptr) return absolute(ptr.getPtrDname());
        if (record instanceof MXResourceRecord mx) return (int) mx.getPreference() + " " + absolute(mx.getExchange());
        return String.valueOf(record.rDataToString());
    }

    // dnslib groups each section into RRsets in first-seen order; the harness lists their records in order.
    static List<ResourceRecord> flatten(List<RRset> rrsets) {
        List<ResourceRecord> out = new ArrayList<>();
        for (RRset rrset : rrsets) out.addAll(rrset.getAll());
        return out;
    }

    static String records(List<ResourceRecord> records) {
        StringBuilder out = new StringBuilder("[");
        for (int i = 0; i < records.size(); i++) {
            AbstractResourceRecord record = (AbstractResourceRecord) records.get(i);
            if (i > 0) out.append(',');
            out.append("{\"name\":").append(quote(absolute(record.getName())))
               .append(",\"type\":").append(record.getRawType())
               .append(",\"class\":").append(record.getRawClassz())
               .append(",\"ttl\":").append(record.getTtl())
               .append(",\"rdata\":").append(quote(rdata(record))).append('}');
        }
        return out.append(']').toString();
    }

    static String questions(List<Question> questions) {
        StringBuilder out = new StringBuilder("[");
        for (int i = 0; i < questions.size(); i++) {
            Question question = questions.get(i);
            if (i > 0) out.append(',');
            out.append("{\"name\":").append(quote(absolute(question.getQName())))
               .append(",\"type\":").append(question.getQTypeValue())
               .append(",\"class\":").append(question.getQClassValue()).append('}');
        }
        return out.append(']').toString();
    }

    static int bit(boolean value) {
        return value ? 1 : 0;
    }

    static String parse(byte[] data) {
        if (data.length == 0 || data.length > 65535) throw new IllegalArgumentException("input outside harness limit");
        Message message = new Message(new NetworkData(data));
        Header header = message.getHeader();
        List<ResourceRecord> answers = flatten(message.getAnswer());
        List<ResourceRecord> authority = flatten(message.getAuthority());
        List<ResourceRecord> additional = flatten(message.getAdditional());
        return "{\"id\":" + header.getId()
            + ",\"qr\":" + bit(header.getQr() == MessageType.RESPONSE)
            + ",\"opcode\":" + header.getRawOpcode()
            + ",\"aa\":" + bit(header.isAa())
            + ",\"tc\":" + bit(header.isTc())
            + ",\"rd\":" + bit(header.isRd())
            + ",\"ra\":" + bit(header.isRa())
            + ",\"z\":" + ((bit(header.isZ()) << 2) | (bit(header.isAd()) << 1) | bit(header.isCd()))
            + ",\"rcode\":" + header.getRawRcode()
            + ",\"qdcount\":" + message.getQuestions().size()
            + ",\"ancount\":" + answers.size()
            + ",\"nscount\":" + authority.size()
            + ",\"arcount\":" + additional.size()
            + ",\"questions\":" + questions(message.getQuestions())
            + ",\"answers\":" + records(answers)
            + ",\"authority\":" + records(authority)
            + ",\"additional\":" + records(additional) + "}";
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (DnsDecodeException | IllegalArgumentException | IllegalStateException
               | IndexOutOfBoundsException | NullPointerException | ClassCastException ignored) { }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("one input path required");
        System.out.write((parse(Files.readAllBytes(Path.of(args[0]))) + "\n").getBytes(StandardCharsets.UTF_8));
        System.out.flush();
    }
}
