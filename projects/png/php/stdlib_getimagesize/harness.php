<?php
declare(strict_types=1);

$path = $argv[1] ?? throw new InvalidArgumentException('PNG path required');
$size = getimagesize($path);
if ($size === false) {
    throw new RuntimeException('getimagesize did not parse PNG');
}
echo json_encode(['width' => $size[0], 'height' => $size[1], 'type' => $size[2]], JSON_THROW_ON_ERROR), "\n";
