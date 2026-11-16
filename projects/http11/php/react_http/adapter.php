<?php
declare(strict_types=1);

require_once __DIR__ . '/vendor/autoload.php';

/** Parse one complete HTTP request through React's server protocol parser. */
function react_parse_request(string $input): array {
    $observed = null;
    $server = new \React\Http\HttpServer(
        static function (\Psr\Http\Message\ServerRequestInterface $request) use (&$observed): \React\Http\Message\Response {
            $observed = [
                'method' => $request->getMethod(),
                'target' => $request->getRequestTarget(),
                'version' => $request->getProtocolVersion(),
                'host' => $request->getHeaderLine('Host'),
                'custom' => $request->getHeaderLine('X-Parsarium'),
            ];
            \React\EventLoop\Loop::stop();
            return new \React\Http\Message\Response(200, ['Content-Length' => '0']);
        }
    );
    $socket = new \React\Socket\SocketServer('127.0.0.1:0');
    $server->listen($socket);
    $client = stream_socket_client($socket->getAddress(), $errno, $error, 1);
    if ($client === false) {
        $socket->close();
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
        $timer = \React\EventLoop\Loop::addTimer(1.0, static function (): void {
            \React\EventLoop\Loop::stop();
        });
        try {
            \React\EventLoop\Loop::run();
        } finally {
            \React\EventLoop\Loop::cancelTimer($timer);
        }
    } finally {
        fclose($client);
        $socket->close();
    }
    if (!is_array($observed)) {
        throw new RuntimeException('React HTTP parser emitted no request');
    }
    return $observed;
}
