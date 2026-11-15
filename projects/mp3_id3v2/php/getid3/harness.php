<?php
declare(strict_types=1);
require_once __DIR__ . '/vendor/autoload.php';
function parsarium_parse_mp3(string $input): array|false
{
    if ($input === '' || strlen($input) > (1 << 20)) return false;
    $path = tempnam('/tmp', 'parsarium-mp3-');
    if ($path === false) throw new RuntimeException('Could not create local input');
    try {
        if (file_put_contents($path, $input) !== strlen($input)) throw new RuntimeException('Could not write local input');
        $parsed = (new getID3())->analyze($path);
        $tags = $parsed['tags']['id3v2'] ?? [];
        return ['title' => $tags['title'][0] ?? null,
                'artist' => $tags['artist'][0] ?? null,
                'album' => $tags['album'][0] ?? null,
                'id3v2_major' => $parsed['id3v2']['majorversion'] ?? null];
    } finally { unlink($path); }
}
