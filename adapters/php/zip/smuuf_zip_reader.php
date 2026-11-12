<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

$reader = new \Smuuf\ZipReader\ZipReader($argv[1]);
$root = $reader->browse('/');
if (!$root instanceof \Smuuf\ZipReader\ZippedDir) {
    throw new RuntimeException('Expected the ZIP root directory');
}
$entries = $root->getEntries();
$name = array_key_first($entries);
$file = $reader->browse($name);
if (!$file instanceof \Smuuf\ZipReader\ZippedFile) {
    throw new RuntimeException('Expected a ZIP file entry');
}
echo json_encode(['entries' => count($entries), 'name' => $name,
                  'content' => $file->read()], JSON_THROW_ON_ERROR), "\n";
