<?php
declare(strict_types=1);

$path = $argv[1] ?? throw new InvalidArgumentException('local SVG path required');
$bytes = file_get_contents($path);
if ($bytes === false) {
    throw new RuntimeException('cannot read SVG control');
}
$file = getimagesize($path);
$memory = getimagesizefromstring($bytes);
$xml = new DOMDocument();
$xmlLoaded = $xml->load($path);
$gdImage = @imagecreatefromstring($bytes);
echo json_encode([
    'file_size' => ['width' => $file[0], 'height' => $file[1], 'mime' => $file['mime'],
        'width_unit' => $file['width_unit'], 'height_unit' => $file['height_unit']],
    'byte_size' => ['width' => $memory[0], 'height' => $memory[1], 'mime' => $memory['mime'],
        'width_unit' => $memory['width_unit'], 'height_unit' => $memory['height_unit']],
    'generic_xml_loaded' => $xmlLoaded,
    'generic_xml_node_type' => $xmlLoaded ? get_class($xml->documentElement) : null,
    'gd_decoded' => $gdImage !== false,
], JSON_THROW_ON_ERROR) . PHP_EOL;
