<?php
declare(strict_types=1);

$path = $argv[1] ?? throw new InvalidArgumentException('input path required');
$bytes = file_get_contents($path);
if ($bytes === false) { throw new RuntimeException('cannot read SVG'); }
$size = getimagesizefromstring($bytes);
if ($size === false) { throw new RuntimeException('getimagesizefromstring did not parse SVG'); }
echo json_encode(['width'=>$size[0], 'height'=>$size[1], 'mime'=>$size['mime'], 'width_unit'=>$size['width_unit'], 'height_unit'=>$size['height_unit']], JSON_THROW_ON_ERROR), "\n";
