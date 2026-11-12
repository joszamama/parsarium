<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

$manager = new \Intervention\Image\ImageManager(new \Intervention\Image\Drivers\Gd\Driver());
$hasher = new \Jenssegers\ImageHash\ImageHash(
    new \Jenssegers\ImageHash\Implementations\AverageHash(), $manager);
$hash = $hasher->hash($argv[1]);
echo json_encode(['average_hash_bits' => $hash->toBits()], JSON_THROW_ON_ERROR), "\n";
