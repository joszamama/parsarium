<?php
declare(strict_types=1);

if ($argc !== 2) {
    throw new InvalidArgumentException('usage: php react_server.php PORT');
}
    require __DIR__ . '/vendor/autoload.php';

$server = new \React\Http\HttpServer(
    static function (\Psr\Http\Message\ServerRequestInterface $request): \React\Http\Message\Response {
        $result = [
            'method' => $request->getMethod(),
            'target' => $request->getRequestTarget(),
            'version' => $request->getProtocolVersion(),
            'host' => $request->getHeaderLine('Host'),
            'custom' => $request->getHeaderLine('X-Parsarium'),
        ];
        return new \React\Http\Message\Response(200, ['Content-Type' => 'application/json'],
            json_encode($result, JSON_THROW_ON_ERROR));
    }
);
$socket = new \React\Socket\SocketServer('127.0.0.1:' . $argv[1]);
$server->listen($socket);
\React\EventLoop\Loop::run();
