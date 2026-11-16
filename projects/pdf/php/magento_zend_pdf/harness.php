<?php
declare(strict_types=1);

function parsarium_parse(string $input): array {
    if ($input === '' || strlen($input) > (1 << 20)) {
        throw new InvalidArgumentException('input outside harness limit');
    }
    $parsariumInputPath = tempnam('/tmp', 'parsarium-pdf-');
    if ($parsariumInputPath === false) { throw new RuntimeException('cannot create parser input'); }
    try {
        if (file_put_contents($parsariumInputPath, $input) !== strlen($input)) {
            throw new RuntimeException('cannot write parser input');
        }
        $argv = ['/work/adapter.php', "magento/zend-pdf", $parsariumInputPath];
        ob_start();
        try { require __DIR__ . '/adapter.php'; $text = (string) ob_get_clean(); }
        catch (Throwable $error) { ob_end_clean(); throw $error; }
        $lines = preg_split('/\r?\n/', trim($text));
        $last = end($lines);
        $observed = json_decode((string) $last, true, 512, JSON_THROW_ON_ERROR);
        if (!is_array($observed)) { throw new RuntimeException('adapter emitted no JSON object'); }
        return $observed;
    } finally { @unlink($parsariumInputPath); }
}
