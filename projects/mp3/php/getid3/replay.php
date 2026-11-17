<?php
declare(strict_types=1);
require __DIR__ . '/harness.php';
$data = file_get_contents($argv[1] ?? '');
if ($data === false) exit(3);
$observed = parsarium_parse_mp3($data);
if ($observed === false) exit(5);
echo json_encode($observed, JSON_THROW_ON_ERROR), "\n";
