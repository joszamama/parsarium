<?php
declare(strict_types=1);
    require __DIR__ . '/vendor/autoload.php';

$image = \Gregwar\Image\Image::open($argv[1]);
echo json_encode(['width' => $image->width(), 'height' => $image->height()],
                 JSON_THROW_ON_ERROR), "\n";
