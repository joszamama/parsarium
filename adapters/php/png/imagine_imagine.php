<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

$image = (new \Imagine\Gd\Imagine())->open($argv[1]);
$size = $image->getSize();
echo json_encode(['width' => $size->getWidth(), 'height' => $size->getHeight()],
                 JSON_THROW_ON_ERROR), "\n";
