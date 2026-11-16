<?php
declare(strict_types=1);

$path = $argv[1] ?? throw new InvalidArgumentException('ZIP path required');
$temporary = tempnam('/tmp', 'parsarium-phar-');
if ($temporary === false) { throw new RuntimeException('cannot create ZIP path'); }
$zipPath = $temporary . '.zip';
rename($temporary, $zipPath);
try {
    if (!copy($path, $zipPath)) { throw new RuntimeException('cannot copy ZIP control'); }
    $archive = new PharData($zipPath);
    $entries = count($archive);
    $name = null; $content = null;
    foreach ($archive as $member) {
        $name = $member->getFilename();
        $content = $member->getContent();
        break;
    }
    if ($entries !== 1 || $name === null || $content === null) { throw new RuntimeException('PharData did not decode ZIP member'); }
    echo json_encode(['entries'=>$entries, 'name'=>$name, 'content'=>$content], JSON_THROW_ON_ERROR), "\n";
} finally { @unlink($zipPath); }
