<?php
declare(strict_types=1);
require_once __DIR__ . '/vendor/autoload.php';

function parsarium_parse_svg(string $input): array|false
{
    if ($input === '' || strlen($input) > (1 << 20)) return false;
    $path = tempnam('/tmp', 'parsarium-svg-');
    if ($path === false) throw new RuntimeException('Could not create local input');
    try {
        if (file_put_contents($path, $input) !== strlen($input)) {
            throw new RuntimeException('Could not write local input');
        }
        $document = new \Svg\Document();
        $document->loadFile($path);
        $size = $document->getDimensions();
        return ['width' => (int) $size['width'], 'height' => (int) $size['height']];
    } finally { unlink($path); }
}
