<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

if ($argc !== 2) {
    exit(2);
}

$provider = new \League\Flysystem\ZipArchive\FilesystemZipArchiveProvider($argv[1]);
$adapter = new \League\Flysystem\ZipArchive\ZipArchiveAdapter($provider);
$entries = iterator_to_array($adapter->listContents('', false));
if (count($entries) === 0) {
    exit(1);
}
$name = $entries[0]->path();
$content = $adapter->read($name);
echo json_encode(['entries' => count($entries), 'name' => $name, 'content' => $content],
                 JSON_THROW_ON_ERROR | JSON_UNESCAPED_SLASHES), PHP_EOL;
