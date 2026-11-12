<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

$archive = new \clsTbsZip();
$archive->DisplayError = false;
if ($archive->Open($argv[1]) !== true) {
    throw new RuntimeException('Failed to open ZIP archive: ' . $archive->Error);
}
try {
    $name = $archive->CdFileLst[0]['v_name'];
    $content = $archive->FileRead($name);
    if ($content === false) {
        throw new RuntimeException('Failed to read ZIP entry: ' . $archive->Error);
    }
    echo json_encode(['entries' => $archive->CdFileNbr, 'name' => $name,
                      'content' => $content], JSON_THROW_ON_ERROR), "\n";
} finally {
    $archive->Close();
}
