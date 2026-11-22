import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;
import io.netty.channel.embedded.EmbeddedChannel;
import io.netty.channel.socket.DatagramPacket;
import io.netty.handler.codec.CorruptedFrameException;
import io.netty.handler.codec.DecoderException;
import io.netty.handler.codec.dns.DatagramDnsQueryDecoder;
import io.netty.handler.codec.dns.DatagramDnsResponseDecoder;
import io.netty.handler.codec.dns.DefaultDnsRecordDecoder;
import io.netty.handler.codec.dns.DnsMessage;
import io.netty.handler.codec.dns.DnsPtrRecord;
import io.netty.handler.codec.dns.DnsQuestion;
import io.netty.handler.codec.dns.DnsRawRecord;
import io.netty.handler.codec.dns.DnsRecord;
import io.netty.handler.codec.dns.DnsRecordType;
import io.netty.handler.codec.dns.DnsResponse;
import io.netty.handler.codec.dns.DnsSection;
import io.netty.util.ReferenceCountUtil;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

/**
 * Local DNS message bytes reach Netty's documented DatagramDnsResponseDecoder (or, when it
 * rejects a non-response, DatagramDnsQueryDecoder) through an EmbeddedChannel. No socket is
 * opened; the DatagramPacket addresses are literal 127.0.0.1 values built without lookup.
 */
public final class NettyDnsHarness {
    private static final InetSocketAddress LOCAL;
    static {
        try {
            LOCAL = new InetSocketAddress(InetAddress.getByAddress(new byte[]{127, 0, 0, 1}), 53);
        } catch (Exception error) {
            throw new ExceptionInInitializerError(error);
        }
    }

    private static DnsMessage decode(byte[] data, boolean response) {
        EmbeddedChannel channel = new EmbeddedChannel(
                response ? new DatagramDnsResponseDecoder() : new DatagramDnsQueryDecoder());
        try {
            channel.writeInbound(new DatagramPacket(Unpooled.wrappedBuffer(data), LOCAL, LOCAL));
            DnsMessage message = channel.readInbound();
            if (message == null) throw new IllegalStateException("decoder produced no message");
            return message;
        } finally {
            channel.finishAndReleaseAll();
        }
    }

    static String absolute(String name) {
        String lower = name.toLowerCase(java.util.Locale.ROOT);
        return lower.endsWith(".") ? lower : lower + ".";
    }

    // RFC 5952 text from the 16 decoded address bytes (Java's own text keeps all zero groups).
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

    static String rdata(DnsRecord record) {
        if (record instanceof DnsPtrRecord ptr) return absolute(ptr.hostname());
        DnsRawRecord raw = (DnsRawRecord) record;
        ByteBuf content = raw.content().duplicate();
        DnsRecordType type = record.type();
        if (type == DnsRecordType.A || type == DnsRecordType.AAAA) {
            byte[] address = new byte[content.readableBytes()];
            content.readBytes(address);
            if (address.length == 4) {
                return (address[0] & 0xff) + "." + (address[1] & 0xff) + "." + (address[2] & 0xff) + "." + (address[3] & 0xff);
            }
            if (address.length == 16) return ipv6(address);
            throw new IllegalArgumentException("address length " + address.length);
        }
        // Netty decompresses CNAME/NS targets and the MX exchange into uncompressed wire names.
        if (type == DnsRecordType.CNAME || type == DnsRecordType.NS) {
            return absolute(DefaultDnsRecordDecoder.decodeName(content));
        }
        if (type == DnsRecordType.MX) {
            int preference = content.readUnsignedShort();
            return preference + " " + absolute(DefaultDnsRecordDecoder.decodeName(content));
        }
        // Netty keeps TXT as a raw record: one or more length-prefixed character-strings.
        if (type == DnsRecordType.TXT) {
            StringBuilder text = new StringBuilder();
            while (content.isReadable()) {
                int length = content.readUnsignedByte();
                byte[] item = new byte[length];
                content.readBytes(item);
                if (text.length() > 0) text.append(' ');
                text.append('"').append(new String(item, StandardCharsets.UTF_8)).append('"');
            }
            return text.toString();
        }
        throw new IllegalArgumentException("record type outside the control subset: " + type);
    }

    static String quote(String value) {
        return "\"" + value.replace("\\", "\\\\").replace("\"", "\\\"") + "\"";
    }

    static String records(DnsMessage message, DnsSection section, boolean question) {
        StringBuilder out = new StringBuilder("[");
        for (int i = 0; i < message.count(section); i++) {
            DnsRecord record = message.recordAt(section, i);
            if (i > 0) out.append(',');
            out.append("{\"name\":").append(quote(absolute(record.name())))
               .append(",\"type\":").append(record.type().intValue())
               .append(",\"class\":").append(record.dnsClass());
            if (!question) {
                out.append(",\"ttl\":").append(record.timeToLive())
                   .append(",\"rdata\":").append(quote(rdata(record)));
            }
            out.append('}');
        }
        return out.append(']').toString();
    }

    static String parse(byte[] data) {
        if (data.length == 0 || data.length > 65535) throw new IllegalArgumentException("input outside harness limit");
        DnsMessage message;
        boolean response = true;
        try {
            message = decode(data, true);
        } catch (DecoderException error) {
            Throwable reason = error instanceof CorruptedFrameException ? error : error.getCause();
            if (!(reason instanceof CorruptedFrameException)
                    || !"not a response".equals(reason.getMessage())) throw error;
            response = false;
            message = decode(data, false);
        }
        try {
            // DnsQuery has no AA, TC, RA or RCODE; a decoded query reports them as 0.
            DnsResponse r = response ? (DnsResponse) message : null;
            return "{\"id\":" + message.id()
                + ",\"qr\":" + (response ? 1 : 0)
                + ",\"opcode\":" + (message.opCode().byteValue() & 0xff)
                + ",\"aa\":" + (r != null && r.isAuthoritativeAnswer() ? 1 : 0)
                + ",\"tc\":" + (r != null && r.isTruncated() ? 1 : 0)
                + ",\"rd\":" + (message.isRecursionDesired() ? 1 : 0)
                + ",\"ra\":" + (r != null && r.isRecursionAvailable() ? 1 : 0)
                + ",\"z\":" + message.z()
                + ",\"rcode\":" + (r != null ? r.code().intValue() : 0)
                + ",\"qdcount\":" + message.count(DnsSection.QUESTION)
                + ",\"ancount\":" + message.count(DnsSection.ANSWER)
                + ",\"nscount\":" + message.count(DnsSection.AUTHORITY)
                + ",\"arcount\":" + message.count(DnsSection.ADDITIONAL)
                + ",\"questions\":" + records(message, DnsSection.QUESTION, true)
                + ",\"answers\":" + records(message, DnsSection.ANSWER, false)
                + ",\"authority\":" + records(message, DnsSection.AUTHORITY, false)
                + ",\"additional\":" + records(message, DnsSection.ADDITIONAL, false) + "}";
        } finally {
            ReferenceCountUtil.release(message);
        }
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (DecoderException | IllegalArgumentException | IllegalStateException | IndexOutOfBoundsException ignored) { }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("one input path required");
        System.out.write((parse(Files.readAllBytes(Path.of(args[0]))) + "\n").getBytes(StandardCharsets.UTF_8));
        System.out.flush();
    }
}
