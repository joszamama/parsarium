<?php
declare(strict_types=1);

$path = $argv[1] ?? throw new InvalidArgumentException('input path required');
$image = imagecreatefrompng($path);
if (!$image instanceof GdImage) { throw new RuntimeException('GD did not decode PNG'); }
// Pixel $index in row-major order. imagecolorat() returns a packed colour on a
// truecolor image and a palette index on a palette image (GD loads palette and
// many grayscale PNGs as palette images), so resolve the index to GD's colour.
function rgb(GdImage $image, int $index): array {
    $width = imagesx($image);
    $pixel = imagecolorat($image, $index % $width, intdiv($index, $width));
    if ($pixel === false) { throw new RuntimeException('cannot read pixel'); }
    if (imageistruecolor($image)) {
        return [($pixel >> 16) & 255, ($pixel >> 8) & 255, $pixel & 255];
    }
    $colour = imagecolorsforindex($image, $pixel);
    return [$colour['red'], $colour['green'], $colour['blue']];
}
$result = ['width'=>imagesx($image), 'height'=>imagesy($image)];
$pixels = imagesx($image) * imagesy($image);
if ($pixels > 0) { $result['left_rgb'] = rgb($image, 0); }
if ($pixels > 1) { $result['right_rgb'] = rgb($image, 1); }
echo json_encode($result, JSON_THROW_ON_ERROR), "\n";
