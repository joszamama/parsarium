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
    'ringcentral/psr7' => 'ringcentral',
    'workerman/psr7' => 'workerman',
    'phly/http' => 'phly',
    'laminas/laminas-diactoros' => 'laminas_diactoros',
    'guzzle/http' => 'guzzle_http',
    'guzzle/guzzle' => 'guzzle_full',
    'innmind/http-parser' => 'innmind',
    'phpstandard/raw-request-factory' => 'phpstandard',
    'angus/laminas-http' => 'angus',
    'workerman/workerman' => 'workerman_server',
    default => throw new InvalidArgumentException('unknown HTTP parser: ' . $package),
};
    require __DIR__ . '/vendor/autoload.php';
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
            // getUrlPartsFromMessage sets query to '' when the path has no '?'; '?' only precedes a query.
            'target' => $request['request_url']['path'] . ($request['request_url']['query'] === '' ? '' : '?' . $request['request_url']['query']),
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
    case 'ringcentral/psr7':
        $request = \RingCentral\Psr7\parse_request($raw);
        $result = [
            'method' => $request->getMethod(),
            'target' => $request->getRequestTarget(),
            'version' => $request->getProtocolVersion(),
            'host' => $request->getHeaderLine('Host'),
            'custom' => $request->getHeaderLine('X-Parsarium'),
        ];
        break;
    case 'workerman/psr7':
        $request = \Workerman\Psr7\parse_request($raw);
        $result = [
            'method' => $request->getMethod(),
            'target' => $request->getRequestTarget(),
            'version' => $request->getProtocolVersion(),
            'host' => $request->getHeaderLine('Host'),
            'custom' => $request->getHeaderLine('X-Parsarium'),
        ];
        break;
    case 'phly/http':
        $request = \Phly\Http\Request\Serializer::fromString($raw);
        $result = [
            'method' => $request->getMethod(),
            'target' => $request->getRequestTarget(),
            'version' => $request->getProtocolVersion(),
            'host' => $request->getHeaderLine('Host'),
            'custom' => $request->getHeaderLine('X-Parsarium'),
        ];
        break;
    case 'laminas/laminas-diactoros':
        $request = \Laminas\Diactoros\Request\Serializer::fromString($raw);
        $result = [
            'method' => $request->getMethod(),
            'target' => $request->getRequestTarget(),
            'version' => $request->getProtocolVersion(),
            'host' => $request->getHeaderLine('Host'),
            'custom' => $request->getHeaderLine('X-Parsarium'),
        ];
        break;
    case 'guzzle/http':
    case 'guzzle/guzzle':
        $request = \Guzzle\Http\Message\RequestFactory::getInstance()->fromMessage($raw);
        $result = [
            'method' => $request->getMethod(),
            'target' => $request->getResource(),
            'version' => $request->getProtocolVersion(),
            'host' => (string) $request->getHeader('Host'),
            'custom' => (string) $request->getHeader('X-Parsarium'),
        ];
        break;
    case 'innmind/http-parser':
        $stream = fopen('php://temp', 'w+');
        fwrite($stream, $raw);
        rewind($stream);
        $read = \Innmind\IO\IO::fromAmbientAuthority()->streams()->acquire($stream)->read();
        $request = \Innmind\HttpParser\Request\Parse::default(\Innmind\Time\Clock::live())($read)
            ->match(
                static fn($parsed) => $parsed,
                static fn() => throw new RuntimeException('Innmind rejected valid HTTP request'),
            );
        $headerValue = static fn(string $name) => $request->headers()->get($name)->match(
            static fn($header) => $header->values()->first()->match(
                static fn($value) => $value->toString(),
                static fn() => null,
            ),
            static fn() => null,
        );
        $result = [
            'method' => $request->method()->toString(),
            'target' => $request->url()->path()->toString() . '?' . $request->url()->query()->toString(),
            'version' => $request->protocolVersion()->toString(),
            'host' => $headerValue('Host'),
            'custom' => $headerValue('X-Parsarium'),
        ];
        break;
    case 'phpstandard/raw-request-factory':
        $psrFactory = new \GuzzleHttp\Psr7\HttpFactory();
        $request = (new \Framework\Http\RawRequestFactory($psrFactory, $psrFactory))
            ->createServerRequest($raw);
        $result = [
            'method' => $request->getMethod(),
            'target' => $request->getRequestTarget(),
            'version' => $request->getProtocolVersion(),
            'host' => $request->getHeaderLine('Host'),
            'custom' => $request->getHeaderLine('X-Parsarium'),
        ];
        break;
    case 'angus/laminas-http':
        $request = \Laminas\Http\Request::fromString($raw);
        $result = [
            'method' => $request->getMethod(),
            'target' => $request->getUriString(),
            'version' => $request->getVersion(),
            'host' => $request->getHeaders()->get('Host')->getFieldValue(),
            'custom' => $request->getHeaders()->get('X-Parsarium')->getFieldValue(),
        ];
        break;
    case 'workerman/workerman':
        $request = new \Workerman\Protocols\Http\Request($raw);
        $result = [
            'method' => $request->method(),
            'target' => $request->uri(),
            'version' => $request->protocolVersion(),
            'host' => $request->header('host'),
            'custom' => $request->header('x-parsarium'),
        ];
        break;
}

echo json_encode($result, JSON_THROW_ON_ERROR), "\n";
