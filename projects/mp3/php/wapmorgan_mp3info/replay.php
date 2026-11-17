<?php
declare(strict_types=1);
require __DIR__ . '/harness.php';
$data = file_get_contents($argv[1] ?? '');
if ($data === false) exit(3);
echo json_encode(parsarium_parse_mp3($data), JSON_THROW_ON_ERROR), "\n";
