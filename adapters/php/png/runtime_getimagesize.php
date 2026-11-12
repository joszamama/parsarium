<?php
declare(strict_types=1);

$info = getimagesize($argv[1]);
if ($info === false) {
    throw new RuntimeException('Could not parse image dimensions');
}
echo json_encode(['width' => $info[0], 'height' => $info[1],
                  'type' => $info[2]], JSON_THROW_ON_ERROR), "\n";
