<?php
declare(strict_types=1);

if ($argc !== 2) {
    exit(2);
}

$archive = new \ZipArchive();
if ($archive->open($argv[1], \ZipArchive::RDONLY) !== true) {
    exit(1);
}
$name = $archive->getNameIndex(0);
$content = $archive->getFromIndex(0);
if ($name === false || $content === false) {
    exit(1);
}
echo json_encode(['entries' => $archive->numFiles, 'name' => $name, 'content' => $content],
                 JSON_THROW_ON_ERROR | JSON_UNESCAPED_SLASHES), PHP_EOL;
$archive->close();
