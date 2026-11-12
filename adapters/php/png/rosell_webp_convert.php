<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

$temporary = tempnam(sys_get_temp_dir(), 'parsarium-webp-');
unlink($temporary);
$destination = $temporary . '.webp';
try {
    \WebPConvert\WebPConvert::convert($argv[1], $destination, ['converter' => 'gd']);
    $info = getimagesize($destination);
    if ($info === false) {
        throw new RuntimeException('WebPConvert did not create a decodable image');
    }
    echo json_encode(['width' => $info[0], 'height' => $info[1],
                      'output_type' => $info[2]], JSON_THROW_ON_ERROR), "\n";
} finally {
    if (is_file($destination)) {
        unlink($destination);
    }
}
