<?php
declare(strict_types=1);

require_once __DIR__ . '/vendor/autoload.php';

function parsarium_parse_wav(string $input): array|false
{
    if ($input === '' || strlen($input) > (1 << 20)) {
        return false;
    }
    $path = tempnam('/tmp', 'parsarium-wav-');
    if ($path === false) {
        throw new RuntimeException('Could not create local input');
    }
    try {
        if (file_put_contents($path, $input) !== strlen($input)) {
            throw new RuntimeException('Could not write local input');
        }
        $parsed = (new getID3())->analyze($path);
        return [
            'fileformat' => $parsed['fileformat'] ?? null,
            'sample_rate' => $parsed['audio']['sample_rate'] ?? null,
            'channels' => $parsed['audio']['channels'] ?? null,
            'bits_per_sample' => $parsed['audio']['bits_per_sample'] ?? null,
        ];
    } finally {
        unlink($path);
    }
}
