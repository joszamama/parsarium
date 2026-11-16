<?php
declare(strict_types=1);

header('Content-Type: application/json');
$headers = getallheaders();
echo json_encode([
    'method' => $_SERVER['REQUEST_METHOD'] ?? null,
    'target' => $_SERVER['REQUEST_URI'] ?? null,
    'version' => preg_replace('~^HTTP/~', '', $_SERVER['SERVER_PROTOCOL'] ?? ''),
    'host' => $headers['Host'] ?? null,
    'custom' => $headers['X-Parsarium'] ?? null,
], JSON_THROW_ON_ERROR), "\n";
