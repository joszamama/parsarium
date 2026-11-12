<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

$type = null;
$image = \Nette\Utils\Image::fromFile($argv[1], $type);
echo json_encode(['width' => $image->getWidth(), 'height' => $image->getHeight(),
                  'type' => $type], JSON_THROW_ON_ERROR), "\n";
