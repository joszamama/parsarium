<?php
declare(strict_types=1);
require __DIR__ . '/harness.php';
$data = file_get_contents($argv[1]);
if ($data === false) exit(2);
parsarium_parse_pnm($data);
