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
}
