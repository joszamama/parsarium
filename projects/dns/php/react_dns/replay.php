<?php
declare(strict_types=1);
require __DIR__ . '/harness.php';
$data = file_get_contents($argv[1]);
if ($data === false) { throw new RuntimeException('cannot read input'); }
echo json_encode(parsarium_parse($data), JSON_THROW_ON_ERROR | JSON_UNESCAPED_SLASHES), "\n";
