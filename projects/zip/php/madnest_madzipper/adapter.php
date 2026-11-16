<?php
declare(strict_types=1);
    require __DIR__ . '/vendor/autoload.php';

$archive = (new \Madnest\Madzipper\Madzipper())->make($argv[1]);
try {
    $entries = $archive->listFiles();
    $name = $entries[0];
    $content = $archive->getFileContent($name);
    if ($content === false) {
        throw new RuntimeException('Failed to read ZIP entry');
    }
    echo json_encode(['entries' => count($entries), 'name' => $name,
                      'content' => $content], JSON_THROW_ON_ERROR), "\n";
} finally {
    $archive->close();
}
