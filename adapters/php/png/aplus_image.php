<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

$image = new \Framework\Image\Image($argv[1]);
echo json_encode(['width' => $image->getWidth(), 'height' => $image->getHeight()], JSON_THROW_ON_ERROR), "\n";
