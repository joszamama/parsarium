<?php
declare(strict_types=1);
    require __DIR__ . '/vendor/autoload.php';

$thief = new \ColorThief\ColorThief(quality: 1, preferredAdapter: 'Gd');
$palette = $thief->getPalette($argv[1], colorCount: 2);
$colors = $palette->toHex('#');
sort($colors);
echo json_encode(['palette' => $colors], JSON_THROW_ON_ERROR), "\n";
