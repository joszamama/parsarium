<?php
declare(strict_types=1);

require_once __DIR__ . '/vendor/autoload.php';

function parsarium_parse_png(string $input): array|false
{
    if ($input === '' || strlen($input) > (1 << 20)) {
        return false;
    }
    $path = tempnam('/tmp', 'parsarium-png-');
    if ($path === false) {
        throw new RuntimeException('Could not create local input');
    }
    try {
        if (file_put_contents($path, $input) !== strlen($input)) {
            throw new RuntimeException('Could not write local input');
        }
        $size = (new \FastImageSize\FastImageSize())->getImageSize($path);
        if ($size === false) {
            return false;
        }
        return ['width' => $size['width'], 'height' => $size['height'], 'type' => $size['type']];
    } finally {
        unlink($path);
    }
}
