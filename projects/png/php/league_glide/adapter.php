<?php
declare(strict_types=1);
    require __DIR__ . '/vendor/autoload.php';

$cache = sys_get_temp_dir() . '/parsarium-glide-' . bin2hex(random_bytes(8));
mkdir($cache, 0700);
try {
    $server = \League\Glide\ServerFactory::create([
        'source' => dirname($argv[1]), 'cache' => $cache, 'driver' => 'gd',
    ]);
    $cached = $server->makeImage(basename($argv[1]), ['fm' => 'png']);
    $bytes = $server->getCache()->read($cached);
    $image = imagecreatefromstring($bytes);
    if ($image === false) {
        throw new RuntimeException('Glide did not create a decodable image');
    }
    echo json_encode(['width' => imagesx($image), 'height' => imagesy($image)], JSON_THROW_ON_ERROR), "\n";
} finally {
    foreach (new RecursiveIteratorIterator(new RecursiveDirectoryIterator($cache, FilesystemIterator::SKIP_DOTS), RecursiveIteratorIterator::CHILD_FIRST) as $item) {
        $item->isDir() ? rmdir($item->getPathname()) : unlink($item->getPathname());
    }
    rmdir($cache);
}
