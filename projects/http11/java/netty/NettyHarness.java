import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import org.jboss.netty.buffer.ChannelBuffers;
import org.jboss.netty.handler.codec.embedder.DecoderEmbedder;
import org.jboss.netty.handler.codec.http.HttpRequest;
import org.jboss.netty.handler.codec.http.HttpRequestDecoder;

public final class NettyHarness {
    record Parsed(String method, String target, String version, String host, String xParsarium) {}

    static Parsed parse(byte[] data) throws IOException {
        if (data.length == 0 || data.length > (1 << 20)) {
            throw new IOException("input outside harness limit");
        }
        var embedder = new DecoderEmbedder<Object>(new HttpRequestDecoder());
        try {
            embedder.offer(ChannelBuffers.wrappedBuffer(data));
            Object value = embedder.poll();
            if (!(value instanceof HttpRequest request)) throw new IOException("incomplete HTTP request");
            return new Parsed(request.getMethod().toString(), request.getUri(),
                              request.getProtocolVersion().toString(),
                              request.headers().get("Host"), request.headers().get("X-Parsarium"));
        } finally { embedder.finish(); }
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (IOException | IllegalArgumentException ignored) { }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("expected control path");
        Parsed p = parse(Files.readAllBytes(Path.of(args[0])));
        System.out.println(json("method", p.method(), "target", p.target(), "version", p.version(),
                                "host", p.host(), "x_parsarium", p.xParsarium()));
    }

    /** Print a flat JSON object; a header the request does not carry is omitted. */
    static String json(String... pairs) {
        StringBuilder out = new StringBuilder("{");
        for (int i = 0; i < pairs.length; i += 2) {
            if (pairs[i + 1] == null) continue;
            if (out.length() > 1) out.append(',');
            out.append('"').append(pairs[i]).append("\":\"");
            for (char c : pairs[i + 1].toCharArray()) {
                if (c == '"' || c == '\\') out.append('\\').append(c);
                else if (c < 0x20) out.append(String.format("\\u%04x", (int) c));
                else out.append(c);
            }
            out.append('"');
        }
        return out.append('}').toString();
    }
}
