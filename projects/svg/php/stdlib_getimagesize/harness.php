<?php
declare(strict_types=1);

$path = $argv[1] ?? throw new InvalidArgumentException('input path required');
$size = getimagesize($path);
if ($size === false) { throw new RuntimeException('getimagesize did not parse SVG'); }
echo json_encode(['width'=>$size[0], 'height'=>$size[1], 'mime'=>$size['mime'], 'width_unit'=>$size['width_unit'], 'height_unit'=>$size['height_unit']], JSON_THROW_ON_ERROR), "\n";
