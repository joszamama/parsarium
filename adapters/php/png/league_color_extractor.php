<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

$palette = \League\ColorExtractor\Palette::fromFilename($argv[1]);
$colors = [];
foreach ($palette->getMostUsedColors() as $color => $count) {
    $colors[sprintf('#%06x', $color)] = $count;
}
ksort($colors);
echo json_encode(['colors' => $colors], JSON_THROW_ON_ERROR), "\n";
