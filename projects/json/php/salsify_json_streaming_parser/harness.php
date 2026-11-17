<?php
declare(strict_types=1);
require __DIR__ . '/vendor/autoload.php';
require __DIR__ . '/summary.php';

use JsonStreamingParser\Listener\IdleListener;
use JsonStreamingParser\Parser;

// Builds stdClass objects and lists from the parser's listener events.
final class ParsariumTreeListener extends IdleListener {
    public mixed $root = null;
    public int $documents = 0;
    private array $stack = [];
    private array $keys = [];

    public function startObject(): void { $this->stack[] = new stdClass(); }
    public function startArray(): void { $this->stack[] = []; }
    public function endObject(): void { $this->insert(array_pop($this->stack)); }
    public function endArray(): void { $this->insert(array_pop($this->stack)); }
    public function key(string $key): void { $this->keys[] = $key; }
    public function value($value): void { $this->insert($value); }
    public function endDocument(): void { $this->documents++; }

    private function insert(mixed $value): void {
        if ($this->stack === []) { $this->root = $value; return; }
        $top = array_key_last($this->stack);
        if ($this->stack[$top] instanceof stdClass) {
            $this->stack[$top]->{array_pop($this->keys)} = $value;
        } else {
            $this->stack[$top][] = $value;
        }
    }
}

function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    $stream = fopen('php://memory', 'w+b');
    fwrite($stream, $input);
    rewind($stream);
    $listener = new ParsariumTreeListener();
    try {
        (new Parser($stream, $listener))->parse();
    } finally {
        fclose($stream);
    }
    // The parser accepts concatenated documents and stops silently at end of stream.
    if ($listener->documents !== 1) {
        throw new InvalidArgumentException('harness requires exactly one complete document');
    }
    return parsarium_json_summary($listener->root);
}
