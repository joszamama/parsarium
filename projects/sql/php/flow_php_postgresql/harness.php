<?php
declare(strict_types=1);
require __DIR__ . '/summary.php';

$path = $argv[1] ?? throw new InvalidArgumentException('input path required');
$bytes = file_get_contents($path);
if ($bytes === false) { throw new RuntimeException('cannot read SQL'); }
// The bytes go to pg_query_parse() in one call; the oracle summary is read from the returned JSON parse tree.
echo json_encode(parsarium_parse($bytes), JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
