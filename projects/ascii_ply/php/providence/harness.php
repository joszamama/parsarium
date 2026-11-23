<?php
declare(strict_types=1);
error_reporting(E_ALL & ~E_DEPRECATED & ~E_USER_DEPRECATED);
define('__CA_LIB_DIR__', __DIR__ . '/support');
require_once __DIR__ . '/parser/PlyToStl.php';
function parsarium_parse_ply(string $input): array|false
{
    if ($input === '' || strlen($input) > (1 << 20)) return false;
    $path = tempnam('/tmp', 'parsarium-ply-');
    $outputPath = tempnam('/tmp', 'parsarium-stl-');
    if ($path === false || $outputPath === false) throw new RuntimeException('Could not create local paths');
    try {
        if (file_put_contents($path, $input) !== strlen($input)) throw new RuntimeException('Could not write local input');
        // PlyToStl::convert returns false, without a message, when it rejects the file.
        if (!PlyToStl::convert($path, $outputPath)) throw new RuntimeException('PlyToStl::convert returned false');
        $stl = file_get_contents($outputPath);
        if ($stl === false) throw new RuntimeException('Could not read converted STL');
        $facets = preg_match_all('/^facet normal\s+/m', $stl);
        preg_match_all('/^\s*vertex\s+(-?\d+(?:\.\d+)?)/m', $stl, $vertices);
        if ($facets === false) throw new RuntimeException('Could not count STL facets');
        $observed = ['facets' => $facets, 'vertices' => count($vertices[1])];
        // second_x is the second STL vertex's x, reported when there is one.
        if (count($vertices[1]) > 1) $observed['second_x'] = (float) $vertices[1][1];
        return $observed;
    } finally { unlink($path); unlink($outputPath); }
}
