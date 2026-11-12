<?php
declare(strict_types=1);

header('Content-Type: application/json');
echo json_encode([
    'method' => $_SERVER['REQUEST_METHOD'] ?? null,
    'target' => $_SERVER['REQUEST_URI'] ?? null,
    'version' => preg_replace('~^HTTP/~', '', $_SERVER['SERVER_PROTOCOL'] ?? ''),
    'host' => getallheaders()['Host'] ?? null,
    'custom' => getallheaders()['X-Parsarium'] ?? null,
], JSON_THROW_ON_ERROR);
