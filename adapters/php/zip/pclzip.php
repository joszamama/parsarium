<?php
declare(strict_types=1);

require __DIR__ . '/pclzip/vendor/autoload.php';

if ($argc !== 2) {
    exit(2);
}

$archive = new \PclZip($argv[1]);
$entries = $archive->extract(PCLZIP_OPT_EXTRACT_AS_STRING);
if ($entries === 0 || count($entries) === 0) {
    exit(1);
}
echo json_encode(['entries' => count($entries), 'name' => $entries[0]['filename'],
                  'content' => $entries[0]['content']],
                 JSON_THROW_ON_ERROR | JSON_UNESCAPED_SLASHES), PHP_EOL;
