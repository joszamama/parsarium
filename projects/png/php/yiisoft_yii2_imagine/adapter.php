<?php
declare(strict_types=1);
    require __DIR__ . '/vendor/autoload.php';
require __DIR__ . '/vendor/yiisoft/yii2/Yii.php';

\yii\imagine\Image::$driver = \yii\imagine\Image::DRIVER_GD2;
// An unbounded box never scales: thumbnail() returns the decoded image at the size it read.
$image = \yii\imagine\Image::thumbnail($argv[1], PHP_INT_MAX, PHP_INT_MAX);
$size = $image->getSize();
echo json_encode(['width' => $size->getWidth(), 'height' => $size->getHeight()], JSON_THROW_ON_ERROR), "\n";
