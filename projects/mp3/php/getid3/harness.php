<?php
declare(strict_types=1);
require_once __DIR__ . '/vendor/autoload.php';
/** Analyze an untagged MPEG audio stream with getID3 and keep the frame-header fields from module.audio.mp3.php. */
function parsarium_parse_mp3(string $input): array|false
{
    if ($input === '' || strlen($input) > (1 << 20)) return false;
    $path = tempnam('/tmp', 'parsarium-mp3-');
    if ($path === false) throw new RuntimeException('Could not create local input');
    try {
        if (file_put_contents($path, $input) !== strlen($input)) throw new RuntimeException('Could not write local input');
        $parsed = (new getID3())->analyze($path);
        $mpeg = $parsed['mpeg']['audio'] ?? null;
        if (($parsed['fileformat'] ?? null) !== 'mp3' || !is_array($mpeg) || !empty($parsed['error'])) return false;
        return ['mpeg_version' => $mpeg['version'] ?? null,
                'layer' => $mpeg['layer'] ?? null,
                'sample_rate' => $mpeg['sample_rate'] ?? null,
                'channels' => $mpeg['channels'] ?? null,
                'channelmode' => $mpeg['channelmode'] ?? null,
                'bitrate' => $mpeg['bitrate'] ?? null,
                'bitrate_mode' => $mpeg['bitrate_mode'] ?? null,
                'framelength' => $mpeg['framelength'] ?? null,
                'playtime_seconds' => isset($parsed['playtime_seconds']) ? round($parsed['playtime_seconds'], 5) : null,
                'audio_data_bytes' => ($parsed['avdataend'] ?? 0) - ($parsed['avdataoffset'] ?? 0),
                'tag_formats' => array_keys($parsed['tags'] ?? [])];
    } finally { unlink($path); }
}
