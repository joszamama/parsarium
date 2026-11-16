<?php
declare(strict_types=1);
function parsarium_parse_pnm(string $input): array|false
{
    if ($input === '' || strlen($input) > (1 << 20)) return false;
    $path = tempnam('/tmp', 'parsarium-pnm-');
    if ($path === false) throw new RuntimeException('Could not create input path');
    try {
        if (file_put_contents($path, $input) !== strlen($input)) throw new RuntimeException('Could not write input');
        $image = new Imagick();
        $image->readImage($path);
        $left = $image->getImagePixelColor(0, 0)->getColor();
        $right = $image->getImagePixelColor(1, 0)->getColor();
        $result = ['width' => $image->getImageWidth(), 'height' => $image->getImageHeight(),
                   'left_rgb' => [$left['r'], $left['g'], $left['b']],
                   'right_rgb' => [$right['r'], $right['g'], $right['b']]];
        $image->clear();
        return $result;
    } catch (ImagickException $e) {
        return false;
    } finally { unlink($path); }
}
