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

    /** Print a flat JSON object; a field whose value the parser did not report is omitted. */
    private static String requestJson(String... pairs) {
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

    private static String headerValue(org.apache.http.Header header) {
        return header == null ? null : header.getValue();
    }

    private static String headerValue(org.apache.hc.core5.http.Header header) {
        return header == null ? null : header.getValue();
    }

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
        else if (args[0].equals("nanohttpd")) runNanoHttpd(bytes);
        else if (args[0].equals("jwarc")) runJwarc(bytes);
        else if (args[0].equals("webarchive")) runWebarchive(bytes);
        else if (args[0].equals("jwat")) runJwat(bytes);
        else if (args[0].equals("sentinel")) runSentinel(bytes);
        else if (args[0].equals("httpcore4nio")) runHttpCore4Nio(bytes);
        else if (args[0].equals("mina")) runMina(bytes);
        else if (args[0].equals("grizzly")) runGrizzly(bytes);
        else if (args[0].equals("jglobus")) runJglobus(bytes);
        else if (args[0].equals("javawarc")) runJavaWarc(bytes);
        else if (args[0].equals("commonshttpclient")) runCommonsHttpClient(bytes);
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
        System.out.println(requestJson("method", method, "target", target, "version", version,
                "host", host, "x_parsarium", marker));
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
        System.out.println(requestJson("method", request.getMethod(),
                "target", request.getRequestUri(), "version", String.valueOf(request.getVersion()),
                "host", headerValue(request.getFirstHeader("Host")),
                "x_parsarium", headerValue(request.getFirstHeader("X-Parsarium"))));
    }

    private static void runHttpCore4(byte[] bytes) throws Exception {
        var buffer = new org.apache.http.impl.io.SessionInputBufferImpl(
                new org.apache.http.impl.io.HttpTransportMetricsImpl(), 1024);
        buffer.bind(new ByteArrayInputStream(bytes));
        var request = new org.apache.http.impl.io.DefaultHttpRequestParser(buffer).parse();
        System.out.println(requestJson("method", request.getRequestLine().getMethod(),
                "target", request.getRequestLine().getUri(),
                "version", String.valueOf(request.getRequestLine().getProtocolVersion()),
                "host", headerValue(request.getFirstHeader("Host")),
                "x_parsarium", headerValue(request.getFirstHeader("X-Parsarium"))));
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
            System.out.println(requestJson("method", String.valueOf(request.method()),
                    "target", request.uri(), "version", String.valueOf(request.protocolVersion()),
                    "host", request.headers().get("Host") == null ? null : request.headers().get("Host").toString(),
                    "x_parsarium", request.headers().get("X-Parsarium") == null ? null
                            : request.headers().get("X-Parsarium").toString()));
            channel.finishAndReleaseAll();
        }
    }

    private static void runJodd(byte[] bytes) {
        var request = jodd.http.HttpRequest.readFrom(new ByteArrayInputStream(bytes));
        String target = request.path() + (request.queryString() == null ? "" : "?" + request.queryString());
        String version = request.httpVersion();
        System.out.println(requestJson("method", request.method(), "target", target, "version", version,
                "host", request.header("Host"), "x_parsarium", request.header("X-Parsarium")));
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

    private static void runNanoHttpd(byte[] bytes) throws Exception {
        final String[] parsed = new String[1];
        var server = new fi.iki.elonen.NanoHTTPD(0) {
            void parse(byte[] input) throws Exception {
                var session = new HTTPSession(new DefaultTempFileManager(),
                        new ByteArrayInputStream(input), new java.io.ByteArrayOutputStream());
                try {
                    session.execute();
                } catch (java.net.SocketException shutdown) {
                    if (parsed[0] == null) throw shutdown;
                }
            }

            @Override
            public fi.iki.elonen.NanoHTTPD.Response serve(fi.iki.elonen.NanoHTTPD.IHTTPSession request) {
                String query = request.getQueryParameterString();
                String target = request.getUri() + (query == null ? "" : "?" + query);
                parsed[0] = requestJson("method", String.valueOf(request.getMethod()), "target", target,
                        "host", request.getHeaders().get("host"),
                        "x_parsarium", request.getHeaders().get("x-parsarium"));
                return fi.iki.elonen.NanoHTTPD.newFixedLengthResponse("");
            }
        };
        server.parse(bytes);
        if (parsed[0] == null) System.exit(1);
        System.out.println(parsed[0]);
    }

    private static void runJwarc(byte[] bytes) throws Exception {
        var channel = java.nio.channels.Channels.newChannel(new ByteArrayInputStream(bytes));
        var request = org.netpreserve.jwarc.HttpRequest.parse(channel);
        System.out.printf("{\"method\":\"%s\",\"target\":\"%s\",\"version\":\"%s\",\"host\":\"%s\",\"x_parsarium\":\"%s\"}%n",
                request.method(), request.target(), request.version(),
                request.headers().first("Host").orElseThrow(),
                request.headers().first("X-Parsarium").orElseThrow());
    }

    private static void runWebarchive(byte[] bytes) throws Exception {
        var request = new org.archive.format.http.HttpRequestParser()
                .parse(new ByteArrayInputStream(bytes));
        if (request.getMessage().isCorrupt() || request.getHeaders().isCorrupt()) System.exit(1);
        System.out.printf("{\"method\":\"%s\",\"target\":\"%s\",\"version\":\"%s\",\"host\":\"%s\",\"x_parsarium\":\"%s\"}%n",
                request.getMessage().getMethodString(), request.getMessage().getPath(),
                request.getMessage().getVersionString(),
                request.getHeaders().getValueCaseInsensitive("Host"),
                request.getHeaders().getValueCaseInsensitive("X-Parsarium"));
    }

    private static void runJwat(byte[] bytes) throws Exception {
        var input = new org.jwat.common.ByteCountingPushBackInputStream(
                new ByteArrayInputStream(bytes), 8192);
        var request = org.jwat.common.HttpHeader.processPayload(
                org.jwat.common.HttpHeader.HT_REQUEST, input, bytes.length, null);
        if (!request.isValid()) System.exit(1);
        var host = request.getHeader("Host");
        var marker = request.getHeader("X-Parsarium");
        if (host == null || marker == null) System.exit(1);
        System.out.printf("{\"method\":\"%s\",\"target\":\"%s\",\"version\":\"%s\",\"host\":\"%s\",\"x_parsarium\":\"%s\"}%n",
                request.method, request.requestUri, request.httpVersion,
                host.value, marker.value);
    }

    private static void runSentinel(byte[] bytes) throws Exception {
        System.setProperty("csp.sentinel.log.output.type", "console");
        var output = System.out;
        com.alibaba.csp.sentinel.transport.heartbeat.client.SimpleHttpResponse response;
        try (var startupMessages = new java.io.PrintStream(new java.io.ByteArrayOutputStream())) {
            System.setOut(startupMessages);
            try {
                response = new com.alibaba.csp.sentinel.transport.heartbeat.client.SimpleHttpResponseParser()
                        .parse(new ByteArrayInputStream(bytes));
            } finally {
                System.setOut(output);
            }
        }
        System.out.printf("{\"status_line\":\"%s\",\"status\":%d,\"content_type\":\"%s\",\"body\":\"%s\"}%n",
                response.getStatusLine(), response.getStatusCode(),
                response.getHeader("Content-Type"), response.getBodyAsString());
    }

    private static void runHttpCore4Nio(byte[] bytes) throws Exception {
        var buffer = new org.apache.http.impl.nio.reactor.SessionInputBufferImpl(1024);
        var parser = new org.apache.http.impl.nio.codecs.DefaultHttpRequestParser(buffer);
        var channel = java.nio.channels.Channels.newChannel(new ByteArrayInputStream(bytes));
        parser.fillBuffer(channel);
        var request = parser.parse();
        if (request == null) System.exit(1);
        System.out.println(requestJson("method", request.getRequestLine().getMethod(),
                "target", request.getRequestLine().getUri(),
                "version", String.valueOf(request.getRequestLine().getProtocolVersion()),
                "host", headerValue(request.getFirstHeader("Host")),
                "x_parsarium", headerValue(request.getFirstHeader("X-Parsarium"))));
    }

    private static void runMina(byte[] bytes) {
        var decoded = new java.util.ArrayList<Object>();
        org.apache.mina.filter.codec.ProtocolDecoderOutput output = new org.apache.mina.filter.codec.ProtocolDecoderOutput() {
            @Override public void write(Object value) { decoded.add(value); }
            @Override public void flush(org.apache.mina.core.filterchain.IoFilter.NextFilter next,
                                        org.apache.mina.core.session.IoSession session) { }
        };
        new org.apache.mina.http.HttpServerDecoder().decode(
                new org.apache.mina.core.session.DummySession(),
                org.apache.mina.core.buffer.IoBuffer.wrap(bytes), output);
        var request = decoded.stream()
                .filter(value -> value instanceof org.apache.mina.http.api.HttpRequest)
                .map(value -> (org.apache.mina.http.api.HttpRequest) value)
                .findFirst().orElseThrow();
        String target = request.getRequestPath()
                + (request.getQueryString() == null ? "" : "?" + request.getQueryString());
        System.out.printf("{\"method\":\"%s\",\"target\":\"%s\",\"version\":\"%s\",\"host\":\"%s\",\"x_parsarium\":\"%s\"}%n",
                request.getMethod(), target, request.getProtocolVersion(),
                request.getHeader("host"), request.getHeader("x-parsarium"));
    }

    private static void runGrizzly(byte[] bytes) throws Exception {
        var transport = org.glassfish.grizzly.nio.transport.TCPNIOTransportBuilder
                .newInstance().build();
        var connection = new org.glassfish.grizzly.nio.transport.TCPNIOConnection(
                transport, null);
        var context = org.glassfish.grizzly.filterchain.FilterChainContext.create(connection);
        context.setMessage(org.glassfish.grizzly.memory.Buffers.wrap(
                org.glassfish.grizzly.memory.MemoryManager.DEFAULT_MEMORY_MANAGER, bytes));
        new org.glassfish.grizzly.http.HttpServerFilter().handleRead(context);
        var content = (org.glassfish.grizzly.http.HttpContent) context.getMessage();
        var request = (org.glassfish.grizzly.http.HttpRequestPacket) content.getHttpHeader();
        String target = request.getRequestURI()
                + (request.getQueryString() == null ? "" : "?" + request.getQueryString());
        System.out.println(requestJson("method", String.valueOf(request.getMethod()), "target", target,
                "version", request.getProtocolString(),
                "host", request.getHeader("Host"), "x_parsarium", request.getHeader("X-Parsarium")));
        context.completeAndRecycle();
    }

    private static void runJglobus(byte[] bytes) throws Exception {
        var response = new org.globus.util.http.HTTPResponseParser(
                new ByteArrayInputStream(bytes));
        System.out.printf("{\"status\":%d,\"message\":\"%s\",\"content_type\":\"%s\",\"content_length\":%d}%n",
                response.getStatusCode(), response.getMessage(),
                response.getContentType(), response.getContentLength());
    }

    private static void runJavaWarc(byte[] bytes) throws Exception {
        var block = new com.github.bottomlessarchive.warc.service.content.response.ResponseContentBlockFactory(
                new com.github.bottomlessarchive.warc.service.header.HeaderParser())
                .newResponseContentBlock(new ByteArrayInputStream(bytes));
        System.out.printf("{\"status\":%d,\"content_type\":\"%s\",\"body\":\"%s\"}%n",
                block.getStatusCode(), block.getMimeType(), block.getPayloadAsString());
    }

    private static void runCommonsHttpClient(byte[] bytes) throws Exception {
        var input = new ByteArrayInputStream(bytes);
        var status = new org.apache.commons.httpclient.StatusLine(
                org.apache.commons.httpclient.HttpParser.readLine(input, "US-ASCII"));
        var headers = org.apache.commons.httpclient.HttpParser.parseHeaders(input, "US-ASCII");
        String contentType = null, contentLength = null;
        for (var header : headers) {
            if (header.getName().equalsIgnoreCase("Content-Type")) contentType = header.getValue();
            if (header.getName().equalsIgnoreCase("Content-Length")) contentLength = header.getValue();
        }
        if (contentType == null || contentLength == null) System.exit(1);
        System.out.printf("{\"version\":\"%s\",\"status\":%d,\"reason\":\"%s\",\"content_type\":\"%s\",\"content_length\":%s}%n",
                status.getHttpVersion(), status.getStatusCode(), status.getReasonPhrase(),
                contentType, contentLength);
    }
}
