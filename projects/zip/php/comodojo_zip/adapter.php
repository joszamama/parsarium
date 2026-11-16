<?php
declare(strict_types=1);
    require __DIR__ . '/vendor/autoload.php';

if ($argc !== 2) {
    exit(2);
}

$archive = \Comodojo\Zip\Zip::open($argv[1]);
$entries = $archive->listFiles();
if (count($entries) === 0) {
    exit(1);
}
$directory = sys_get_temp_dir() . '/parsarium-zip-' . bin2hex(random_bytes(8));
mkdir($directory);
try {
    $archive->extract($directory);
    $content = file_get_contents($directory . '/' . $entries[0]);
    if ($content === false) {
        exit(1);
    }
    echo json_encode(['entries' => count($entries), 'name' => $entries[0], 'content' => $content],
                     JSON_THROW_ON_ERROR | JSON_UNESCAPED_SLASHES), PHP_EOL;
} finally {
    $archive->close();
    @unlink($directory . '/' . $entries[0]);
    @rmdir($directory);
}
