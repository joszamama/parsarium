<?php
declare(strict_types=1);

$path = $argv[1] ?? throw new InvalidArgumentException('usage: php runtime_probe.php CONTROL');
echo json_encode([
    'fileinfo_loaded' => extension_loaded('fileinfo'),
    'fileinfo_mime' => (new finfo(FILEINFO_MIME_TYPE))->file($path),
    'getimagesize' => @getimagesize($path) !== false,
    'gd_loaded' => extension_loaded('gd'),
    'imagecreatefromstring' => @imagecreatefromstring(file_get_contents($path)) !== false,
    'ffi_loaded' => extension_loaded('FFI'),
], JSON_THROW_ON_ERROR), "\n";
