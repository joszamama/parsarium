<?php
declare(strict_types=1);

$bytes = file_get_contents($argv[1]);
if ($bytes === false) {
    throw new RuntimeException('Could not read control bytes');
}
$info = getimagesizefromstring($bytes);
if ($info === false) {
    throw new RuntimeException('Could not parse image dimensions');
}
echo json_encode(['width' => $info[0], 'height' => $info[1],
                  'type' => $info[2]], JSON_THROW_ON_ERROR), "\n";
