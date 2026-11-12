<?php
declare(strict_types=1);

if ($argc !== 2) {
    exit(2);
}

$archive = new \PharData($argv[1]);
$entries = iterator_to_array($archive);
if (count($entries) === 0) {
    exit(1);
}
$first = array_values($entries)[0];
echo json_encode(['entries' => count($entries), 'name' => $first->getFilename(),
                  'content' => $first->getContent()],
                 JSON_THROW_ON_ERROR | JSON_UNESCAPED_SLASHES), PHP_EOL;
