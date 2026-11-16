<?php
declare(strict_types=1);

$path = $argv[1] ?? throw new InvalidArgumentException('input path required');
$image = imagecreatefrompng($path);
if (!$image instanceof GdImage) { throw new RuntimeException('GD did not decode PNG'); }
function rgb(GdImage $image, int $x): array {
    $pixel = imagecolorat($image, $x, 0);
    if ($pixel === false) { throw new RuntimeException('cannot read pixel'); }
    return [($pixel >> 16) & 255, ($pixel >> 8) & 255, $pixel & 255];
}
echo json_encode(['width'=>imagesx($image), 'height'=>imagesy($image), 'left_rgb'=>rgb($image, 0), 'right_rgb'=>rgb($image, 1)], JSON_THROW_ON_ERROR), "\n";
