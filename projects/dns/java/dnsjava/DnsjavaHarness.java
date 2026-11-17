import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Locale;
import org.xbill.DNS.AAAARecord;
import org.xbill.DNS.Flags;
import org.xbill.DNS.Header;
import org.xbill.DNS.Message;
import org.xbill.DNS.Record;
import org.xbill.DNS.Section;
import org.xbill.DNS.WireParseException;

/** Local DNS message bytes reach dnsjava's documented Message(byte[]) constructor. No resolver is used. */
public final class DnsjavaHarness {
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

    static String rdata(Record record) {
        // AAAA uses the decoded 16 bytes; the other types use dnsjava's own presentation text.
        if (record instanceof AAAARecord aaaa) return ipv6(aaaa.getAddress().getAddress());
        String text = record.rdataToString();
        return switch (record.getType()) {
            case 5, 2, 12 -> absolute(text);
            case 15 -> {
                String[] parts = text.split(" ", 2);
                yield parts[0] + " " + absolute(parts[1]);
            }
            default -> text;
        };
    }

    static String section(Message message, int section, boolean question) {
        List<Record> records = message.getSection(section);
        StringBuilder out = new StringBuilder("[");
        for (int i = 0; i < records.size(); i++) {
            Record record = records.get(i);
            if (i > 0) out.append(',');
            out.append("{\"name\":").append(quote(absolute(record.getName().toString())))
               .append(",\"type\":").append(record.getType())
               .append(",\"class\":").append(record.getDClass());
            if (!question) {
                out.append(",\"ttl\":").append(record.getTTL())
                   .append(",\"rdata\":").append(quote(rdata(record)));
            }
            out.append('}');
        }
        return out.append(']').toString();
    }

    static int bit(Header header, int flag) {
        return header.getFlag(flag) ? 1 : 0;
    }

    static String parse(byte[] data) throws java.io.IOException {
        if (data.length == 0 || data.length > 65535) throw new IllegalArgumentException("input outside harness limit");
        Message message = new Message(data);
        Header header = message.getHeader();
        return "{\"id\":" + header.getID()
            + ",\"qr\":" + bit(header, Flags.QR)
            + ",\"opcode\":" + header.getOpcode()
            + ",\"aa\":" + bit(header, Flags.AA)
            + ",\"tc\":" + bit(header, Flags.TC)
            + ",\"rd\":" + bit(header, Flags.RD)
            + ",\"ra\":" + bit(header, Flags.RA)
            + ",\"z\":" + ((bit(header, 9) << 2) | (bit(header, Flags.AD) << 1) | bit(header, Flags.CD))
            + ",\"rcode\":" + header.getRcode()
            + ",\"qdcount\":" + header.getCount(Section.QUESTION)
            + ",\"ancount\":" + header.getCount(Section.ANSWER)
            + ",\"nscount\":" + header.getCount(Section.AUTHORITY)
            + ",\"arcount\":" + header.getCount(Section.ADDITIONAL)
            + ",\"questions\":" + section(message, Section.QUESTION, true)
            + ",\"answers\":" + section(message, Section.ANSWER, false)
            + ",\"authority\":" + section(message, Section.AUTHORITY, false)
            + ",\"additional\":" + section(message, Section.ADDITIONAL, false) + "}";
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (WireParseException | IllegalArgumentException ignored) { }
        catch (java.io.IOException ignored) { }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("one input path required");
        System.out.write((parse(Files.readAllBytes(Path.of(args[0]))) + "\n").getBytes(StandardCharsets.UTF_8));
        System.out.flush();
    }
}
