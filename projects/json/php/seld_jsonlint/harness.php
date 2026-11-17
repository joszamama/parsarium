<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';
require __DIR__ . '/summary.php';

function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    $decoded = (new \Seld\JsonLint\JsonParser())->parse($input);
    return parsarium_json_summary($decoded);
}
