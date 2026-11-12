<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

$manager = \Intervention\Image\ImageManager::usingDriver(
    \Intervention\Image\Drivers\Gd\Driver::class
);
$image = $manager->decodePath($argv[1]);
echo json_encode(['width' => $image->width(), 'height' => $image->height()],
                 JSON_THROW_ON_ERROR), "\n";
