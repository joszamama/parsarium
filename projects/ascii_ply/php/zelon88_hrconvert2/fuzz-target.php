<?php
declare(strict_types=1);
require __DIR__ . '/harness.php';
$data = file_get_contents($argv[1]);
if ($data === false) exit(2);
$result = parsarium_parse_ply($data);
if ($result === false) exit(1);
echo json_encode($result, JSON_THROW_ON_ERROR), "\n";
