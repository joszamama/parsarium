<?php
declare(strict_types=1);
require_once __DIR__ . '/parser/ModelMetadataExtractor.php';
function parsarium_parse_ply(string $input): array|false
{
    if ($input === '' || strlen($input) > (1 << 20)) return false;
    $path = tempnam('/tmp', 'parsarium-ply-');
    if ($path === false) throw new RuntimeException('Could not create local path');
    try {
        if (file_put_contents($path, $input) !== strlen($input)) throw new RuntimeException('Could not write input');
        $metadata = (new Ahg3dModel\Services\ModelMetadataExtractor())->extract($path, 'ply');
        if (!isset($metadata['vertex_count'], $metadata['face_count'])) return false;
        return ['vertices' => $metadata['vertex_count'], 'faces' => $metadata['face_count']];
    } finally { unlink($path); }
}
