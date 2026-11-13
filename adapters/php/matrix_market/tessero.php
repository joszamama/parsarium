<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

if ($argc !== 2) {
    fwrite(STDERR, "Expected a local Matrix Market control path\n");
    exit(2);
}
$bytes = file_get_contents($argv[1]);
if ($bytes === false) {
    fwrite(STDERR, "Could not read local control\n");
    exit(3);
}
$matrix = Tessero\Io\MatrixMarket::read($bytes);
$entries = 0;
foreach ($matrix['data'] as $row) {
    foreach ($row as $value) {
        if ($value != 0) {
            $entries++;
        }
    }
}
echo json_encode([
    'rows' => $matrix['rows'],
    'cols' => $matrix['cols'],
    'format' => $matrix['format'],
    'entries' => $entries,
    'value_1_3' => $matrix['data'][0][2],
], JSON_THROW_ON_ERROR), "\n";
