<?php
/* Replay Heratio's tagged PLY metadata extractor against a local file. */
if ($argc !== 3 || !is_file($argv[1]) || !is_file($argv[2])) {
    exit(2);
}
require $argv[2];
$metadata = (new Ahg3dModel\Services\ModelMetadataExtractor())->extract($argv[1], 'ply');
if (!isset($metadata['vertex_count'], $metadata['face_count'])) {
    fwrite(STDERR, "PLY element counts were not parsed\n");
    exit(1);
}
echo json_encode([
    'vertices' => $metadata['vertex_count'],
    'faces' => $metadata['face_count'],
], JSON_THROW_ON_ERROR), "\n";
