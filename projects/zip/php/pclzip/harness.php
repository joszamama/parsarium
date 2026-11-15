<?php
declare(strict_types=1);

require_once __DIR__ . '/vendor/autoload.php';

function parsarium_parse_zip(string $input): array|false
{
    if ($input === '' || strlen($input) > (1 << 20)) {
        return false;
    }
    $path = tempnam('/tmp', 'parsarium-zip-');
    if ($path === false) {
        throw new RuntimeException('Could not create local input');
    }
    try {
        if (file_put_contents($path, $input) !== strlen($input)) {
            throw new RuntimeException('Could not write local input');
        }
        $archive = new PclZip($path);
        $entries = $archive->extract(PCLZIP_OPT_EXTRACT_AS_STRING);
        if (!is_array($entries) || count($entries) === 0) {
            return false;
        }
        $first = $entries[0];
        if (strlen($first['content']) > (1 << 20)) {
            return false;
        }
        return ['entries' => count($entries), 'name' => $first['filename'],
                'content' => $first['content']];
    } finally {
        unlink($path);
    }
}
