<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';

use Cerbero\JsonParser\JsonParser;
use Cerbero\JsonParser\Tokens\Parser;

// Builds an ordered type-tagged tree with the documented lazy() mode: every nested
// object and array stays a Tokens\Parser walked by the package's own Lexer and
// Parser, so the default JsonDecoder (json_decode) only sees single key and scalar
// tokens. The eager default would hand whole member subtrees to json_decode.
function parsarium_compound(iterable $members, string $kind): array {
    $node = $kind === 'object' ? ['type' => 'object', 'members' => []] : ['type' => 'array', 'items' => []];
    $seen = [];
    foreach ($members as $key => $value) {
        $child = $value instanceof Parser ? parsarium_compound($value, parsarium_kind($value)) : parsarium_scalar($value);
        if ($kind === 'array') {
            if ($key !== count($node['items'])) {
                throw new UnexpectedValueException('array member without next integer index');
            }
            $node['items'][] = $child;
        } else {
            if (!is_string($key) || isset($seen[$key])) {
                throw new UnexpectedValueException('object member without unique string key');
            }
            $seen[$key] = true;
            $node['members'][] = [$key, $child];
        }
    }
    return $node;
}

// A lazy Parser does not say whether it holds an object or an array (both are
// empty when the compound is). Its first token is the package Lexer's own
// CompoundBegin; reading it through the public lazyLoad() before iteration
// starts leaves the shared token stream at the same position.
function parsarium_kind(Parser $parser): string {
    return match ((string) $parser->lazyLoad()->current()) {
        '{' => 'object',
        '[' => 'array',
    };
}

function parsarium_scalar(mixed $value): array {
    return match (true) {
        $value === null => ['type' => 'null'],
        is_bool($value) => ['type' => 'boolean', 'value' => $value],
        is_int($value) => ['type' => 'integer', 'value' => (string) $value],
        is_float($value) => ['type' => 'float', 'value' => $value],
        is_string($value) => ['type' => 'string', 'value' => $value],
    };
}

function parsarium_tree(JsonParser $parser, string $kind): array {
    return parsarium_compound($parser->lazy(), $kind);
}

// String sources go through JsonParser's source dispatch, which treats a string
// naming a local file or an http(s) URL as that source; the harness keeps to
// JSON text by requiring an object or array root. Member keys and array indexes
// above confirm the root kind for non-empty roots.
function parsarium_root_kind(string $input): string {
    $first = substr(ltrim($input, " \t\r\n"), 0, 1);
    if ($first !== '{' && $first !== '[') {
        throw new InvalidArgumentException('harness supports object/array roots');
    }
    return $first === '{' ? 'object' : 'array';
}

function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    return parsarium_tree(JsonParser::parse($input), parsarium_root_kind($input));
}

// No-parse baseline for the AFL++ bridge: same input checks, no package call.
function parsarium_no_parse(string $input): array {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    return ['root' => parsarium_root_kind($input)];
}
