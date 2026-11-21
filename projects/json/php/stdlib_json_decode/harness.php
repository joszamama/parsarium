<?php
declare(strict_types=1);
require __DIR__ . '/summary.php';

$path = $argv[1] ?? throw new InvalidArgumentException('input path required');
$bytes = file_get_contents($path);
if ($bytes === false) { throw new RuntimeException('cannot read JSON'); }
$decoded = json_decode($bytes, false, 512, JSON_THROW_ON_ERROR);
echo parsarium_json_text(parsarium_json_summary($decoded), JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE), "\n";
