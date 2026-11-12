package org.parsarium;

import io.netty.buffer.Unpooled;
import io.netty.channel.embedded.EmbeddedChannel;
import io.netty.handler.codec.http.HttpRequest;
import io.netty.handler.codec.http.HttpRequestDecoder;
import java.nio.file.Files;
import java.nio.file.Path;
import java.io.ByteArrayInputStream;
import java.nio.ByteBuffer;
import io.micrometer.core.instrument.simple.SimpleMeterRegistry;
import org.webpieces.data.api.DataWrapperGeneratorFactory;
import org.webpieces.data.impl.BufferCreationPool;
import org.webpieces.httpparser.api.HttpParser;
import org.webpieces.httpparser.api.HttpParserFactory;
import org.webpieces.httpparser.api.Memento;
import org.webpieces.httpparser.api.common.Header;

public final class Http11Adapter {
    private Http11Adapter() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 2) System.exit(2);
        byte[] bytes = Files.readAllBytes(Path.of(args[1]));
        if (args[0].equals("netty")) runNetty(bytes);
        else if (args[0].equals("webpieces")) runWebpieces(bytes);
        else if (args[0].equals("httpcore5")) runHttpCore5(bytes);
        else if (args[0].equals("httpcore4")) runHttpCore4(bytes);
        else if (args[0].equals("jetty")) runJetty(bytes);
        else if (args[0].equals("netty3")) runNetty3(bytes);
        else if (args[0].equals("netty5")) runNetty5(bytes);
        else if (args[0].equals("jodd")) runJodd(bytes);
        else if (args[0].equals("rawhttp")) runRawHttp(bytes);
        else System.exit(2);
    }

    private static void runNetty(byte[] bytes) {
        EmbeddedChannel channel = new EmbeddedChannel(new HttpRequestDecoder());
        channel.writeInbound(Unpooled.wrappedBuffer(bytes));
        Object value = channel.readInbound();
        if (!(value instanceof HttpRequest)) {
            channel.finishAndReleaseAll();
            System.exit(1);
        }
        HttpRequest request = (HttpRequest) value;
        if (!request.decoderResult().isSuccess()) {
            channel.finishAndReleaseAll();
            System.exit(1);
        }
        String method = request.method().name();
        String target = request.uri();
        String version = request.protocolVersion().text();
        String host = request.headers().get("Host");
        String marker = request.headers().get("X-Parsarium");
        if (host == null || marker == null) {
            channel.finishAndReleaseAll();
            System.exit(1);
        }
        System.out.printf("{\"method\":\"%s\",\"target\":\"%s\",\"version\":\"%s\",\"host\":\"%s\",\"x_parsarium\":\"%s\"}%n",
                method, target, version, host, marker);
        channel.finishAndReleaseAll();
    }

    private static void runWebpieces(byte[] bytes) {
        SimpleMeterRegistry metrics = new SimpleMeterRegistry();
        HttpParser parser = HttpParserFactory.createParser("parsarium", metrics,
                new BufferCreationPool(metrics));
        Memento state = parser.parse(parser.prepareToParse(),
                DataWrapperGeneratorFactory.createDataWrapperGenerator().wrapByteArray(bytes));
        org.webpieces.httpparser.api.dto.HttpRequest request = state.getParsedMessages().stream()
                .filter(value -> value instanceof org.webpieces.httpparser.api.dto.HttpRequest)
                .map(value -> (org.webpieces.httpparser.api.dto.HttpRequest) value)
                .findFirst().orElseThrow();
        String method = request.getRequestLine().getMethod().toString();
        String target = request.getRequestLine().getUri().getUri();
        String version = request.getRequestLine().getVersion().toString();
        String host = null, marker = null;
        for (Header header : request.getHeaders()) {
            if (header.getName().equalsIgnoreCase("Host")) host = header.getValue();
            if (header.getName().equalsIgnoreCase("X-Parsarium")) marker = header.getValue();
        }
        if (host == null || marker == null) System.exit(1);
        System.out.printf("{\"method\":\"%s\",\"target\":\"%s\",\"version\":\"%s\",\"host\":\"%s\",\"x_parsarium\":\"%s\"}%n",
                method, target, version, host, marker);
        metrics.close();
    }

    private static void runHttpCore5(byte[] bytes) throws Exception {
        var buffer = new org.apache.hc.core5.http.impl.io.SessionInputBufferImpl(1024);
        var request = new org.apache.hc.core5.http.impl.io.DefaultHttpRequestParser()
                .parse(buffer, new ByteArrayInputStream(bytes));
        System.out.printf("{\"method\":\"%s\",\"target\":\"%s\",\"version\":\"%s\",\"host\":\"%s\",\"x_parsarium\":\"%s\"}%n",
                request.getMethod(), request.getRequestUri(), request.getVersion(),
                request.getFirstHeader("Host").getValue(),
                request.getFirstHeader("X-Parsarium").getValue());
    }

    private static void runHttpCore4(byte[] bytes) throws Exception {
        var buffer = new org.apache.http.impl.io.SessionInputBufferImpl(
                new org.apache.http.impl.io.HttpTransportMetricsImpl(), 1024);
        buffer.bind(new ByteArrayInputStream(bytes));
        var request = new org.apache.http.impl.io.DefaultHttpRequestParser(buffer).parse();
        System.out.printf("{\"method\":\"%s\",\"target\":\"%s\",\"version\":\"%s\",\"host\":\"%s\",\"x_parsarium\":\"%s\"}%n",
                request.getRequestLine().getMethod(), request.getRequestLine().getUri(),
                request.getRequestLine().getProtocolVersion(),
                request.getFirstHeader("Host").getValue(),
                request.getFirstHeader("X-Parsarium").getValue());
    }

    private static void runJetty(byte[] bytes) {
        var request = org.eclipse.jetty.http.HttpTester.parseRequest(ByteBuffer.wrap(bytes));
        if (request == null || !request.isComplete()) System.exit(1);
        System.out.printf("{\"method\":\"%s\",\"target\":\"%s\",\"version\":\"%s\",\"host\":\"%s\",\"x_parsarium\":\"%s\"}%n",
                request.getMethod(), request.getURI(), request.getVersion(),
                request.getLast(org.eclipse.jetty.http.HttpHeader.HOST), request.get("X-Parsarium"));
    }

    private static void runNetty3(byte[] bytes) {
        var embedder = new org.jboss.netty.handler.codec.embedder.DecoderEmbedder<Object>(
                new org.jboss.netty.handler.codec.http.HttpRequestDecoder());
        embedder.offer(org.jboss.netty.buffer.ChannelBuffers.wrappedBuffer(bytes));
        Object value = embedder.poll();
        if (!(value instanceof org.jboss.netty.handler.codec.http.HttpRequest)) System.exit(1);
        var request = (org.jboss.netty.handler.codec.http.HttpRequest) value;
        System.out.printf("{\"method\":\"%s\",\"target\":\"%s\",\"version\":\"%s\",\"host\":\"%s\",\"x_parsarium\":\"%s\"}%n",
                request.getMethod(), request.getUri(), request.getProtocolVersion(),
                request.headers().get("Host"), request.headers().get("X-Parsarium"));
        embedder.finish();
    }

    private static void runNetty5(byte[] bytes) {
        try (var allocator = io.netty5.buffer.BufferAllocator.onHeapUnpooled()) {
            var channel = new io.netty5.channel.embedded.EmbeddedChannel(
                    new io.netty5.handler.codec.http.HttpRequestDecoder());
            channel.writeInbound(allocator.copyOf(bytes));
            Object value = channel.readInbound();
            if (!(value instanceof io.netty5.handler.codec.http.HttpRequest)) {
                channel.finishAndReleaseAll();
                System.exit(1);
            }
            var request = (io.netty5.handler.codec.http.HttpRequest) value;
            System.out.printf("{\"method\":\"%s\",\"target\":\"%s\",\"version\":\"%s\",\"host\":\"%s\",\"x_parsarium\":\"%s\"}%n",
                    request.method(), request.uri(), request.protocolVersion(),
                    request.headers().get("Host"), request.headers().get("X-Parsarium"));
            channel.finishAndReleaseAll();
        }
    }

    private static void runJodd(byte[] bytes) {
        var request = jodd.http.HttpRequest.readFrom(new ByteArrayInputStream(bytes));
        String target = request.path() + (request.queryString() == null ? "" : "?" + request.queryString());
        String version = request.httpVersion();
        System.out.printf("{\"method\":\"%s\",\"target\":\"%s\",\"version\":\"%s\",\"host\":\"%s\",\"x_parsarium\":\"%s\"}%n",
                request.method(), target, version, request.header("Host"), request.header("X-Parsarium"));
    }

    private static void runRawHttp(byte[] bytes) throws Exception {
        var request = new rawhttp.core.RawHttp().parseRequest(new ByteArrayInputStream(bytes));
        var uri = request.getUri();
        String target = uri.getRawPath() + (uri.getRawQuery() == null ? "" : "?" + uri.getRawQuery());
        System.out.printf("{\"method\":\"%s\",\"target\":\"%s\",\"version\":\"%s\",\"host\":\"%s\",\"x_parsarium\":\"%s\"}%n",
                request.getMethod(), target, request.getStartLine().getHttpVersion(),
                request.getHeaders().getFirst("Host").orElseThrow(),
                request.getHeaders().getFirst("X-Parsarium").orElseThrow());
    }
}
