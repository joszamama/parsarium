<?php
declare(strict_types=1);
    require __DIR__ . '/vendor/autoload.php';

if ($argc !== 2) {
    exit(2);
}

$archive = \Alchemy\Zippy\Adapter\ZipExtensionAdapter::newInstance()->open($argv[1]);
$entries = array_values($archive->getMembers());
if (count($entries) === 0) {
    exit(1);
}
$name = $entries[0]->getLocation();
$directory = sys_get_temp_dir() . '/parsarium-zip-' . bin2hex(random_bytes(8));
mkdir($directory);
try {
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
