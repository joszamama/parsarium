<?php
declare(strict_types=1);
    require __DIR__ . '/vendor/autoload.php';
date_default_timezone_set('UTC');

$archive = \ezcArchive::open($argv[1], \ezcArchive::ZIP,
                            new \ezcArchiveOptions(['readOnly' => true]));
$directory = sys_get_temp_dir() . '/parsarium-zeta-' . bin2hex(random_bytes(8));
mkdir($directory);
try {
    $entries = [];
    foreach ($archive as $entry) {
        $entries[] = $entry->getPath();
        $archive->extractCurrent($directory);
    }
    $name = $entries[0];
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
