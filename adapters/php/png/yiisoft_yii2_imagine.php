<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';
require __DIR__ . '/vendor/yiisoft/yii2/Yii.php';

\yii\imagine\Image::$driver = \yii\imagine\Image::DRIVER_GD2;
$image = \yii\imagine\Image::thumbnail($argv[1], 2, 1);
$size = $image->getSize();
echo json_encode(['width' => $size->getWidth(), 'height' => $size->getHeight()], JSON_THROW_ON_ERROR), "\n";
