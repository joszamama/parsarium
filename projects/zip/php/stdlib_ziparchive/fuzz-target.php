<?php
declare(strict_types=1);

$path = $argv[1] ?? null;
if ($path === null || !is_file($path) || filesize($path) > (1 << 20)) { exit(0); }
$archive = new ZipArchive();
try {
    if (@$archive->open($path, ZipArchive::RDONLY) === true) {
        if ($archive->numFiles > 0) { @$archive->getFromIndex(0); }
        $archive->close();
    }
} catch (Throwable) { }
