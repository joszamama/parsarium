<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

$app = new \Illuminate\Container\Container();
\Illuminate\Support\Facades\Facade::setFacadeApplication($app);
$app->instance(\Intervention\Image\Laravel\Facades\Image::BINDING,
    \Intervention\Image\ImageManager::usingDriver(\Intervention\Image\Drivers\Gd\Driver::class));
$image = \Intervention\Image\Laravel\Facades\Image::decodePath($argv[1]);
echo json_encode(['width' => $image->width(), 'height' => $image->height()], JSON_THROW_ON_ERROR), "\n";
