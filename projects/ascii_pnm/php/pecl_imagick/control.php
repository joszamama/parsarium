<?php
declare(strict_types=1);
require __DIR__ . '/harness.php';
$data = file_get_contents($argv[1]);
if ($data === false) throw new RuntimeException('Could not read input');
$result = parsarium_parse_pnm($data);
if ($result === false) throw new RuntimeException('PECL Imagick did not decode PNM control');
echo json_encode($result, JSON_THROW_ON_ERROR), "\n";
