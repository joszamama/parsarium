<?php
declare(strict_types=1);

require_once __DIR__ . '/adapter.php';

function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    return react_parse_request($input);
}
