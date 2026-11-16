<?php
declare(strict_types=1);
    require __DIR__ . '/vendor/autoload.php';

if ($argc !== 2) {
    exit(2);
}

$archive = \wapmorgan\UnifiedArchive\UnifiedArchive::open($argv[1]);
$entries = $archive->getFiles();
if (count($entries) === 0) {
    exit(1);
}
$content = $archive->getFileContent($entries[0]);
echo json_encode(['entries' => count($entries), 'name' => $entries[0], 'content' => $content],
                 JSON_THROW_ON_ERROR | JSON_UNESCAPED_SLASHES), PHP_EOL;
