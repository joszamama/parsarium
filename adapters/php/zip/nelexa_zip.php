<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

if ($argc !== 2) {
    exit(2);
}

$archive = (new \PhpZip\ZipFile())->openFile($argv[1]);
$names = $archive->getListFiles();
if (count($names) === 0) {
    exit(1);
}
$content = $archive->getEntryContents($names[0]);
$result = ['entries' => count($names), 'name' => $names[0], 'content' => $content];
echo json_encode($result, JSON_THROW_ON_ERROR | JSON_UNESCAPED_SLASHES), PHP_EOL;
$archive->close();
