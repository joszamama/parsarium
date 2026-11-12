<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

$size = (new \FastImageSize\FastImageSize())->getImageSize($argv[1]);
if ($size === false) {
    throw new RuntimeException('Could not parse PNG dimensions');
}
echo json_encode(['width' => $size['width'], 'height' => $size['height'],
                  'type' => $size['type']], JSON_THROW_ON_ERROR), "\n";
