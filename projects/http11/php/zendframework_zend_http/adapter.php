<?php
declare(strict_types=1);

if ($argc !== 3) {
    throw new InvalidArgumentException('usage: php parse_legacy.php PACKAGE CONTROL');
}
$package = $argv[1];
$path = $argv[2];
$projects = [
    'zendframework/zend-http' => 'zend_http',
    'zendframework/zend-diactoros' => 'zend_diactoros',
    'vircom/http-parser' => 'vircom',
];
if (!isset($projects[$package])) {
    throw new InvalidArgumentException('unknown legacy HTTP parser: ' . $package);
}
    require __DIR__ . '/vendor/autoload.php';
$raw = file_get_contents($path);
if ($raw === false) {
    throw new RuntimeException('cannot read control: ' . $path);
}

if ($package === 'zendframework/zend-http') {
    $request = \Zend\Http\Request::fromString($raw);
    $result = [
        'method' => $request->getMethod(),
        'target' => $request->getUriString(),
        'version' => $request->getVersion(),
        'host' => $request->getHeaders()->get('Host'),
        'custom' => $request->getHeaders()->get('X-Parsarium'),
    ];
    // Headers::get() returns false for a header the request does not carry; omit that field.
    foreach (['host', 'custom'] as $field) {
        if ($result[$field] === false) { unset($result[$field]); }
        else { $result[$field] = $result[$field]->getFieldValue(); }
    }
} elseif ($package === 'zendframework/zend-diactoros') {
    $request = \Zend\Diactoros\Request\Serializer::fromString($raw);
    $result = [
        'method' => $request->getMethod(),
        'target' => $request->getRequestTarget(),
        'version' => $request->getProtocolVersion(),
        'host' => $request->getHeaderLine('Host'),
        'custom' => $request->getHeaderLine('X-Parsarium'),
    ];
} else {
    $request = (new \VirCom\HttpParser\HttpParserFactory())->createRequestParser()->parse($raw);
    $headers = [];
    foreach ($request->getHeaders() as $header) {
        $values = $header->getValues();
        $headers[strtolower($header->getName())] = $values[0] ?? null;
    }
    $result = [
        'method' => $request->getStartLine()->getHttpMethod()->getValue(),
        'target' => $request->getStartLine()->getTargetRequest(),
        'version' => preg_replace('~^HTTP/~', '', $request->getStartLine()->getHttpVersion()->getValue()),
        'host' => $headers['host'] ?? null,
        'custom' => $headers['x-parsarium'] ?? null,
    ];
}

echo json_encode($result, JSON_THROW_ON_ERROR), "\n";
