<?php
declare(strict_types=1);

[$script, $path] = $argv + [null, null];
if ($path === null) {
    throw new InvalidArgumentException('usage: php runtime_probe.php CONTROL');
}

echo json_encode([
    'id3_extension_loaded' => extension_loaded('id3'),
    'id3_get_tag_exists' => function_exists('id3_get_tag'),
    'fileinfo_mime' => (new finfo(FILEINFO_MIME_TYPE))->file($path),
], JSON_THROW_ON_ERROR), "\n";
