<?php
declare(strict_types=1);

$path = $argv[1] ?? throw new InvalidArgumentException('ZIP path required');
$archive = new ZipArchive();
if ($archive->open($path, ZipArchive::RDONLY) !== true) { throw new RuntimeException('ZipArchive did not parse ZIP'); }
try {
    if ($archive->numFiles !== 1) { throw new RuntimeException('expected one ZIP member'); }
    $name = $archive->getNameIndex(0);
    $content = $archive->getFromIndex(0);
    if ($name === false || $content === false) { throw new RuntimeException('could not decode ZIP member'); }
    $observed = ['entries'=>$archive->numFiles, 'name'=>$name, 'content'=>$content];
} finally { $archive->close(); }
echo json_encode($observed, JSON_THROW_ON_ERROR), "\n";
