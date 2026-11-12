<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

$cache = sys_get_temp_dir() . '/parsarium-contao-' . bin2hex(random_bytes(8));
mkdir($cache, 0700);
try {
    $source = new \Contao\Image\Image($argv[1], new \Imagine\Gd\Imagine());
    $config = (new \Contao\Image\ResizeConfiguration())->setWidth(1)->setHeight(1);
    $resized = (new \Contao\Image\Resizer($cache, 'parsarium-valid-control'))
        ->resize($source, $config, (new \Contao\Image\ResizeOptions())->setBypassCache(true));
    $info = getimagesize($resized->getPath());
    if ($info === false) {
        throw new RuntimeException('Contao did not create a decodable image');
    }
    echo json_encode(['width' => $info[0], 'height' => $info[1], 'type' => $info[2]], JSON_THROW_ON_ERROR), "\n";
} finally {
    foreach (new RecursiveIteratorIterator(new RecursiveDirectoryIterator($cache, FilesystemIterator::SKIP_DOTS), RecursiveIteratorIterator::CHILD_FIRST) as $item) {
        $item->isDir() ? rmdir($item->getPathname()) : unlink($item->getPathname());
    }
    rmdir($cache);
}
