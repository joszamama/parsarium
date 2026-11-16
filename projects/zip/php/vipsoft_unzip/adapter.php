<?php
declare(strict_types=1);
    require __DIR__ . '/vendor/autoload.php';

if ($argc !== 2) {
    exit(2);
}

$directory = sys_get_temp_dir() . '/parsarium-zip-' . bin2hex(random_bytes(8));
mkdir($directory);
try {
    $entries = (new \VIPSoft\Unzip\Unzip())->extract($argv[1], $directory);
    if (count($entries) === 0) {
        exit(1);
    }
    $content = file_get_contents($directory . '/' . $entries[0]);
    if ($content === false) {
        exit(1);
    }
    echo json_encode(['entries' => count($entries), 'name' => $entries[0], 'content' => $content],
                     JSON_THROW_ON_ERROR | JSON_UNESCAPED_SLASHES), PHP_EOL;
} finally {
    foreach (glob($directory . '/*') ?: [] as $file) {
        @unlink($file);
    }
    @rmdir($directory);
}
