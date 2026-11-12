<?php
declare(strict_types=1);

[$script, $package, $path] = $argv + [null, null, null];
if ($package === null || $path === null) {
    throw new InvalidArgumentException('usage: php parse.php PACKAGE CONTROL');
}

$project = match ($package) {
    'guzzlehttp/psr7' => 'guzzle_psr7',
    'laminas/laminas-http' => 'laminas_http',
    'guzzle/parser' => 'guzzle_parser',
    'alexpts/http-message-parser' => 'alexpts',
    'sekjun9878/request-parser' => 'sekjun',
    default => throw new InvalidArgumentException('unknown HTTP parser: ' . $package),
};
require __DIR__ . '/' . $project . '/vendor/autoload.php';
$raw = file_get_contents($path);
if ($raw === false) {
    throw new RuntimeException('cannot read control: ' . $path);
}

switch ($package) {
    case 'guzzlehttp/psr7':
        $request = \GuzzleHttp\Psr7\Message::parseRequest($raw);
        $result = [
            'method' => $request->getMethod(),
            'target' => $request->getRequestTarget(),
            'version' => $request->getProtocolVersion(),
            'host' => $request->getHeaderLine('Host'),
            'custom' => $request->getHeaderLine('X-Parsarium'),
        ];
        break;
    case 'laminas/laminas-http':
        $request = \Laminas\Http\Request::fromString($raw);
        $result = [
            'method' => $request->getMethod(),
            'target' => $request->getUriString(),
            'version' => $request->getVersion(),
            'host' => $request->getHeaders()->get('Host')->getFieldValue(),
            'custom' => $request->getHeaders()->get('X-Parsarium')->getFieldValue(),
        ];
        break;
    case 'guzzle/parser':
        $request = (new \Guzzle\Parser\Message\MessageParser())->parseRequest($raw);
        $result = [
            'method' => $request['method'],
            'target' => $request['request_url']['path'] . '?' . $request['request_url']['query'],
            'version' => $request['version'],
            'host' => $request['headers']['Host'],
            'custom' => $request['headers']['X-Parsarium'],
        ];
        break;
    case 'alexpts/http-message-parser':
        $request = (new \PTS\ParserPsr7\Factory\Psr7Factory())->toPsr7Request($raw);
        $result = [
            'method' => $request->getMethod(),
            'target' => $request->getUri()->getPath() . '?' . $request->getUri()->getQuery(),
            'version' => $request->getProtocolVersion(),
            'host' => $request->getHeaderLine('Host'),
            'custom' => $request->getHeaderLine('X-Parsarium'),
        ];
        break;
    case 'sekjun9878/request-parser':
        $parser = new \sekjun9878\RequestParser\RequestParser();
        $parser->addData($raw);
        $request = \sekjun9878\RequestParser\Request::create($parser->exportRequestState());
        $headers = $request->getHeaders();
        $result = [
            'method' => $request->getMethod(),
            'target' => $request->getUrl(),
            'version' => preg_replace('~^HTTP/~', '', $request->getProtocolVersion()),
            'host' => $headers['Host'] ?? $headers['host'] ?? null,
            'custom' => $headers['X-Parsarium'] ?? $headers['x-parsarium'] ?? null,
        ];
        break;
}

echo json_encode($result, JSON_THROW_ON_ERROR), "\n";
