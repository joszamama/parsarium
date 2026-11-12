<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

$directory = sys_get_temp_dir() . '/parsarium-joomla-' . bin2hex(random_bytes(8));
mkdir($directory);
try {
    $archive = new \Joomla\Archive\Archive(['tmp_path' => sys_get_temp_dir()]);
    if ($archive->extract($argv[1], $directory) !== true) {
        throw new RuntimeException('ZIP extraction failed');
    }
    $entries = array_values(array_diff(scandir($directory), ['.', '..']));
    $name = $entries[0];
    $content = file_get_contents($directory . '/' . $name);
    if ($content === false) {
        throw new RuntimeException('Failed to read extracted ZIP entry');
    }
    echo json_encode(['entries' => count($entries), 'name' => $name,
                      'content' => $content], JSON_THROW_ON_ERROR), "\n";
} finally {
    if (isset($name) && is_file($directory . '/' . $name)) {
        unlink($directory . '/' . $name);
    }
    rmdir($directory);
}
