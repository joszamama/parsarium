<?php
declare(strict_types=1);

require __DIR__ . '/mmoreram/vendor/autoload.php';

$directory = new \Mmoreram\Extractor\Filesystem\TemporaryDirectory();
$extractor = new \Mmoreram\Extractor\Extractor($directory);
try {
    $entries = iterator_to_array($extractor->extractFromFile($argv[1]), false);
    $file = $entries[0];
    $name = $file->getFilename();
    $content = file_get_contents($file->getRealPath());
    if ($content === false) {
        throw new RuntimeException('Failed to read extracted ZIP entry');
    }
    echo json_encode(['entries' => count($entries), 'name' => $name,
                      'content' => $content], JSON_THROW_ON_ERROR), "\n";
} finally {
    if (isset($file) && is_file($file->getRealPath())) {
        unlink($file->getRealPath());
    }
    if (is_dir($directory->getDirectoryPath())) {
        rmdir($directory->getDirectoryPath());
    }
}
