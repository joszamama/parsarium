<?php
declare(strict_types=1);

require_once __DIR__ . '/vendor/autoload.php';

/** Parse one complete HTTP request through Amp's HTTP server driver. */
function amp_parse_request(string $input): array {
    $observed = null;
    $suspension = \Revolt\EventLoop::getSuspension();
    $record = static function (\Amp\Http\Server\Request $request) use (&$observed, $suspension): void {
        $uri = $request->getUri();
        $observed = [
            'method' => $request->getMethod(),
            // getQuery() is '' when the request target has no query; '?' only precedes a query.
            'target' => $uri->getPath() . ($uri->getQuery() === '' ? '' : '?' . $uri->getQuery()),
            'version' => $request->getProtocolVersion(),
            'host' => $request->getHeader('Host'),
            'custom' => $request->getHeader('X-Parsarium'),
        ];
        \Revolt\EventLoop::defer(static function () use ($suspension): void {
            $suspension->resume();
        });
    };
    $handler = new class($record) implements \Amp\Http\Server\RequestHandler {
        public function __construct(private \Closure $record) {}
        public function handleRequest(\Amp\Http\Server\Request $request): \Amp\Http\Server\Response {
            ($this->record)($request);
            return new \Amp\Http\Server\Response(200, ['Content-Length' => '0']);
        }
    };
    $server = \Amp\Http\Server\SocketHttpServer::createForDirectAccess(new \Psr\Log\NullLogger());
    $server->expose('127.0.0.1:0');
    $server->start($handler, new \Amp\Http\Server\DefaultErrorHandler());
    $address = $server->getServers()[0]->getAddress()->toString();
    $client = stream_socket_client('tcp://' . $address, $errno, $error, 1);
    if ($client === false) {
        $server->stop();
        throw new RuntimeException("cannot connect to local parser: $error ($errno)");
    }
    try {
        $written = 0;
        while ($written < strlen($input)) {
            $count = fwrite($client, substr($input, $written));
            if ($count === false || $count === 0) {
                throw new RuntimeException('cannot write request to local parser');
            }
            $written += $count;
        }
        $timer = \Revolt\EventLoop::delay(1.0, static function () use ($suspension): void {
            $suspension->resume();
        });
        try {
            $suspension->suspend();
        } finally {
            \Revolt\EventLoop::cancel($timer);
        }
    } finally {
        fclose($client);
        $server->stop();
    }
    if (!is_array($observed)) {
        throw new RuntimeException('Amp HTTP parser emitted no request');
    }
    return $observed;
}
