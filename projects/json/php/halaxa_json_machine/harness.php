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
    $first = substr(ltrim($input), 0, 1);
    if ($first !== '{' && $first !== '[') {
        throw new InvalidArgumentException('harness supports object/array roots');
    }
    $root = $first === '{' ? new stdClass() : [];
    foreach (Items::fromString($input, ['decoder' => new ExtJsonDecoder()]) as $key => $value) {
        if ($root instanceof stdClass) {
            $root->{(string) $key} = $value;
        } else {
            $root[] = $value;
        }
    }
    return parsarium_json_summary($root);
}
