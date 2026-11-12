<?php
declare(strict_types=1);

$bytes = file_get_contents($argv[1]);
if ($bytes === false) {
    throw new RuntimeException('Could not read control bytes');
}
$image = imagecreatefromstring($bytes);
if ($image === false) {
    throw new RuntimeException('Could not decode PNG bytes');
}
$left = imagecolorat($image, 0, 0);
$right = imagecolorat($image, 1, 0);
echo json_encode(['width' => imagesx($image), 'height' => imagesy($image),
                  'left_rgb' => [($left >> 16) & 255, ($left >> 8) & 255, $left & 255],
                  'right_rgb' => [($right >> 16) & 255, ($right >> 8) & 255, $right & 255]],
                 JSON_THROW_ON_ERROR), "\n";
