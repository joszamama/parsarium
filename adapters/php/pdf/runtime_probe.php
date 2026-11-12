<?php
declare(strict_types=1);

[$script, $path] = $argv + [null, null];
if ($path === null) {
    throw new InvalidArgumentException('usage: php runtime_probe.php CONTROL');
}

$bytes = file_get_contents($path);
if ($bytes === false) {
    throw new RuntimeException('cannot read PDF control');
}
$image = @imagecreatefromstring($bytes);
echo json_encode([
    'fileinfo_loaded' => extension_loaded('fileinfo'),
    'fileinfo_mime' => (new finfo(FILEINFO_MIME_TYPE))->file($path),
    'gd_loaded' => extension_loaded('gd'),
    'getimagesize' => @getimagesize($path) !== false,
    'imagecreatefromstring' => $image !== false,
], JSON_THROW_ON_ERROR), "\n";
