<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

$image = (new \claviska\SimpleImage())->fromFile($argv[1]);
$left = $image->getColorAt(0, 0);
$right = $image->getColorAt(1, 0);
echo json_encode(['width' => $image->getWidth(), 'height' => $image->getHeight(),
                  'left_rgb' => [$left['red'], $left['green'], $left['blue']],
                  'right_rgb' => [$right['red'], $right['green'], $right['blue']]],
                 JSON_THROW_ON_ERROR), "\n";
