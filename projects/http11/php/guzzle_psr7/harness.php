<?php
declare(strict_types=1);
require_once __DIR__ . '/vendor/autoload.php';
function parsarium_parse_http11(string $input): array|false
{
    if ($input === '' || strlen($input) > (1 << 20)) return false;
    $request = \GuzzleHttp\Psr7\Message::parseRequest($input);
    return ['method' => $request->getMethod(),
            'target' => $request->getRequestTarget(),
            'version' => $request->getProtocolVersion(),
            'host' => $request->getHeaderLine('Host'),
            'custom' => $request->getHeaderLine('X-Parsarium')];
}
