<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';
require __DIR__ . '/summary.php';

use JsonMachine\Items;
use JsonMachine\JsonDecoder\ExtJsonDecoder;

function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    // JSON Machine scans the document's members; ext/json decodes each value.
    // JSON Machine itself rejects a scalar root with a SyntaxErrorException.
    $first = substr(ltrim($input), 0, 1);
    $root = $first === '{' ? new ParsariumObject() : [];
    foreach (Items::fromString($input, ['decoder' => new ExtJsonDecoder()]) as $key => $value) {
        if ($root instanceof ParsariumObject) {
            $root->members[(string) $key] = $value;
        } else {
            $root[] = $value;
        }
    }
    return parsarium_json_summary($root);
}
