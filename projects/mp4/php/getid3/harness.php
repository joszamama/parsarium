<?php
declare(strict_types=1);
require_once __DIR__ . '/vendor/autoload.php';
function parsarium_parse_mp4(string $input): array|false
{
    if ($input === '' || strlen($input) > (1 << 20)) return false;
    $path = tempnam('/tmp', 'parsarium-mp4-');
    if ($path === false) throw new RuntimeException('Could not create local input');
    try {
        if (file_put_contents($path, $input) !== strlen($input)) throw new RuntimeException('Could not write local input');
        $parsed = (new getID3())->analyze($path);
        return ['format' => $parsed['fileformat'] ?? null,
                'width' => $parsed['video']['resolution_x'] ?? null,
                'height' => $parsed['video']['resolution_y'] ?? null,
                'video_fourcc' => $parsed['video']['fourcc'] ?? null,
                'audio_channels' => $parsed['audio']['channels'] ?? null];
    } finally { unlink($path); }
}
