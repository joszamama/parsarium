<?php
declare(strict_types=1);

require __DIR__ . '/chumper/vendor/autoload.php';

$archive = (new \Chumper\Zipper\Zipper())->make($argv[1]);
$content = $archive->getFileContent('hello.txt');
if ($content === false) {
    throw new RuntimeException('Failed to read ZIP entry');
}
echo json_encode(['content' => $content], JSON_THROW_ON_ERROR), "\n";
