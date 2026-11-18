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
    $observed = ['entries'=>count($archive)];
    // Read every member PharData lists (directories are traversed, not read);
    // report the first member in PharData's own iteration order.
    $members = new RecursiveIteratorIterator($archive, RecursiveIteratorIterator::SELF_FIRST);
    foreach ($members as $member) {
        $name = substr($member->getPathname(), strlen('phar://' . $zipPath . '/'));
        $content = $member->isDir() ? '' : $member->getContent();
        if (!array_key_exists('name', $observed)) { $observed['name'] = $name; $observed['content'] = $content; }
    }
    echo json_encode($observed, JSON_THROW_ON_ERROR), "\n";
} finally { @unlink($zipPath); }
