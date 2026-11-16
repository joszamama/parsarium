<?php
declare(strict_types=1);

if ($argc !== 2) {
    throw new InvalidArgumentException('usage: php amphp_server.php PORT');
}
    require __DIR__ . '/vendor/autoload.php';

$handler = new class implements \Amp\Http\Server\RequestHandler {
    public function handleRequest(\Amp\Http\Server\Request $request): \Amp\Http\Server\Response
    {
        $uri = $request->getUri();
        $result = [
            'method' => $request->getMethod(),
            'target' => $uri->getPath() . '?' . $uri->getQuery(),
            'version' => $request->getProtocolVersion(),
            'host' => $request->getHeader('Host'),
            'custom' => $request->getHeader('X-Parsarium'),
        ];
        return new \Amp\Http\Server\Response(
            200,
            ['Content-Type' => 'application/json'],
            json_encode($result, JSON_THROW_ON_ERROR),
        );
    }
};

$server = \Amp\Http\Server\SocketHttpServer::createForDirectAccess(new \Psr\Log\NullLogger());
$server->expose('127.0.0.1:' . $argv[1]);
$server->start($handler, new \Amp\Http\Server\DefaultErrorHandler());
\Revolt\EventLoop::run();
