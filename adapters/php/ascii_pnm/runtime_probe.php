<?php
declare(strict_types=1);

$path = $argv[1] ?? throw new InvalidArgumentException('missing control path');
$bytes = file_get_contents($path);
if ($bytes === false) {
    throw new RuntimeException('cannot read control');
}

echo json_encode([
    'getimagesize' => @getimagesize($path) !== false,
    'getimagesizefromstring' => @getimagesizefromstring($bytes) !== false,
    'imagecreatefromstring' => @imagecreatefromstring($bytes) !== false,
], JSON_THROW_ON_ERROR), "\n";
