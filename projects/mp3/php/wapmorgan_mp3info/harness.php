<?php
declare(strict_types=1);
require_once __DIR__ . '/vendor/autoload.php';

use wapmorgan\Mp3Info\Mp3Info;

/** Read an untagged MPEG audio stream with Mp3Info's documented constructor and keep its frame-header fields. */
function parsarium_parse_mp3(string $input): array
{
    if ($input === '' || strlen($input) > (1 << 20)) throw new InvalidArgumentException('input outside harness limit');
    $path = tempnam('/tmp', 'parsarium-mp3-');
    if ($path === false) throw new RuntimeException('Could not create local input');
    try {
        if (file_put_contents($path, $input) !== strlen($input)) throw new RuntimeException('Could not write local input');
        $audio = new Mp3Info($path);
        return ['mpeg_version' => $audio->codecVersion,
                'layer' => $audio->layerVersion,
                'sample_rate' => $audio->sampleRate,
                'channel' => $audio->channel,
                'bitrate' => $audio->bitRate,
                'is_vbr' => $audio->isVbr,
                'audio_size' => $audio->audioSize,
                'frames' => (int) $audio->_framesCount, // ceil() estimate is a float on CBR input
                'duration' => round($audio->duration, 5)];
    } finally { unlink($path); }
}
