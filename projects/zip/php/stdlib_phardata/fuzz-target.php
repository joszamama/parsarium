<?php
declare(strict_types=1);

$path = $argv[1] ?? null;
if ($path === null || !is_file($path) || filesize($path) > (1 << 20)) { exit(0); }
$temporary = tempnam('/tmp', 'parsarium-phar-');
if ($temporary === false) { exit(0); }
$zipPath = $temporary . '.zip';
rename($temporary, $zipPath);
try {
    if (copy($path, $zipPath)) {
        try {
            $archive = new PharData($zipPath);
            foreach ($archive as $member) { $member->getContent(); break; }
        } catch (Throwable) { }
    }
} finally { @unlink($zipPath); }
