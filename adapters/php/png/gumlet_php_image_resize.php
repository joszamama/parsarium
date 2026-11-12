<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

$image = new \Gumlet\ImageResize($argv[1]);
echo json_encode(['width' => $image->getSourceWidth(),
                  'height' => $image->getSourceHeight()], JSON_THROW_ON_ERROR), "\n";
