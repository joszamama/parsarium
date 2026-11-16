<?php
declare(strict_types=1);
    require __DIR__ . '/vendor/autoload.php';

$layer = \PHPImageWorkshop\ImageWorkshop::initFromPath($argv[1]);
echo json_encode(['width' => $layer->getWidth(), 'height' => $layer->getHeight()], JSON_THROW_ON_ERROR), "\n";
