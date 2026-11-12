<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

$archive = \Macellan\Zip\Zip::open($argv[1]);
$entries = $archive->listFiles();
$name = $entries[0];
$directory = sys_get_temp_dir() . '/parsarium-macellan-' . bin2hex(random_bytes(8));
try {
    $archive->extract($directory, $name);
    $content = file_get_contents($directory . '/' . $name);
    if ($content === false) {
        throw new RuntimeException('Failed to read extracted ZIP entry');
    }
    echo json_encode(['entries' => count($entries), 'name' => $name,
                      'content' => $content], JSON_THROW_ON_ERROR), "\n";
} finally {
    $archive->close();
    if (is_file($directory . '/' . $name)) {
        unlink($directory . '/' . $name);
    }
    if (is_dir($directory)) {
        rmdir($directory);
    }
}
