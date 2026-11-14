<?php
/* Replay Providence's released PLY-to-STL parser against a local file. */
error_reporting(E_ALL & ~E_DEPRECATED & ~E_USER_DEPRECATED);

if ($argc !== 3 || !is_file($argv[1]) || !is_file($argv[2])) {
    exit(2);
}

// The parser has a legacy Db.php include, but its convert path never uses Db.
define('__CA_LIB_DIR__', __DIR__ . '/support');
require $argv[2];

$outputPath = tempnam(sys_get_temp_dir(), 'parsarium-ply-stl-');
if ($outputPath === false) {
    exit(1);
}
try {
    if (!PlyToStl::convert($argv[1], $outputPath)) {
        throw new RuntimeException('Providence PLY conversion failed');
    }
    $stl = file_get_contents($outputPath);
    if ($stl === false) {
        throw new RuntimeException('Cannot read converted STL');
    }
    $facets = preg_match_all('/^facet normal\s+/m', $stl);
    preg_match_all('/^\s*vertex\s+(-?\d+(?:\.\d+)?)/m', $stl, $vertices);
    if ($facets === false || count($vertices[1]) < 2) {
        throw new RuntimeException('Converted geometry is incomplete');
    }
    echo json_encode([
        'facets' => $facets,
        'vertices' => count($vertices[1]),
        'second_x' => (float) $vertices[1][1],
    ], JSON_THROW_ON_ERROR), "\n";
} finally {
    unlink($outputPath);
}
