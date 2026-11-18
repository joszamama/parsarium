<?php
declare(strict_types=1);

$path = $argv[1] ?? throw new InvalidArgumentException('ZIP path required');
$archive = new ZipArchive();
$status = $archive->open($path, ZipArchive::RDONLY);
if ($status !== true) { throw new RuntimeException("ZipArchive::open failed with code $status"); }
try {
    $observed = ['entries'=>$archive->numFiles];
    // Read every member in central-directory order; report the first one.
    for ($index = 0; $index < $archive->numFiles; $index++) {
        $name = $archive->getNameIndex($index);
        $content = $archive->getFromIndex($index);
        if ($name === false || $content === false) {
            throw new RuntimeException('ZipArchive could not read member ' . $index . ': ' . $archive->getStatusString());
        }
        if ($index === 0) { $observed['name'] = $name; $observed['content'] = $content; }
    }
} finally { $archive->close(); }
echo json_encode($observed, JSON_THROW_ON_ERROR), "\n";
