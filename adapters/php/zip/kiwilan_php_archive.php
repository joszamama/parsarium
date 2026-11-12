<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

$archive = \Kiwilan\Archive\Archive::read($argv[1]);
$item = $archive->getFirst();
$name = $item->getPath();
$content = $archive->getContents($item);
if ($content === null) {
    throw new RuntimeException('Failed to read ZIP entry');
}
echo json_encode(['entries' => $archive->getCount(), 'name' => $name,
                  'content' => $content], JSON_THROW_ON_ERROR), "\n";
