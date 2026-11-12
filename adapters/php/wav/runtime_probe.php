<?php
declare(strict_types=1);

$path = $argv[1] ?? throw new InvalidArgumentException('usage: php runtime_probe.php CONTROL');
$finfo = new finfo(FILEINFO_MIME_TYPE);
echo json_encode([
    'fileinfo_loaded' => extension_loaded('fileinfo'),
    'fileinfo_mime' => $finfo->file($path),
    'ffi_loaded' => extension_loaded('FFI'),
], JSON_THROW_ON_ERROR), "\n";
