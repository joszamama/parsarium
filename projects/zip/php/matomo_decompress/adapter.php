<?php
declare(strict_types=1);
    require __DIR__ . '/vendor/autoload.php';

$directory = sys_get_temp_dir() . '/parsarium-matomo-' . bin2hex(random_bytes(8));
mkdir($directory);
try {
    $reader = new \Matomo\Decompress\ZipArchive($argv[1]);
    $entries = $reader->extract($directory);
    if (!is_array($entries) || count($entries) === 0) {
        throw new RuntimeException('ZIP extraction failed');
    }
    $name = $entries[0]['stored_filename'];
    $content = file_get_contents($directory . '/' . $name);
    if ($content === false) {
        throw new RuntimeException('Failed to read extracted ZIP entry');
    }
    echo json_encode(['entries' => count($entries), 'name' => $name,
                      'content' => $content], JSON_THROW_ON_ERROR), "\n";
} finally {
    if (isset($name) && is_file($directory . '/' . $name)) {
        unlink($directory . '/' . $name);
    }
    rmdir($directory);
}
