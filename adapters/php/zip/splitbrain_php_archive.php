<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

if ($argc !== 2) {
    exit(2);
}

$archive = new \splitbrain\PHPArchive\Zip();
$archive->open($argv[1]);
$entries = $archive->contents();
if (count($entries) === 0) {
    exit(1);
}
$name = $entries[0]->getPath();
$directory = sys_get_temp_dir() . '/parsarium-zip-' . bin2hex(random_bytes(8));
mkdir($directory);
try {
    $archive->open($argv[1]);
    $archive->extract($directory);
    $content = file_get_contents($directory . '/' . $name);
    if ($content === false) {
        exit(1);
    }
    echo json_encode(['entries' => count($entries), 'name' => $name, 'content' => $content],
                     JSON_THROW_ON_ERROR | JSON_UNESCAPED_SLASHES), PHP_EOL;
} finally {
    @unlink($directory . '/' . $name);
    @rmdir($directory);
}
