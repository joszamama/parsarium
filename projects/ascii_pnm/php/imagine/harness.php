<?php
declare(strict_types=1);

require_once __DIR__ . '/vendor/autoload.php';

function parsarium_parse_pnm(string $input): array|false
{
    if ($input === '' || strlen($input) > (1 << 20)) {
        return false;
    }
    $path = tempnam('/tmp', 'parsarium-pnm-');
    if ($path === false) {
        throw new RuntimeException('Could not create local input');
    }
    try {
        if (file_put_contents($path, $input) !== strlen($input)) {
            throw new RuntimeException('Could not write local input');
        }
        $image = (new \Imagine\Imagick\Imagine())->open($path);
        $size = $image->getSize();
        return ['width' => $size->getWidth(), 'height' => $size->getHeight()];
    } finally {
        unlink($path);
    }
}
