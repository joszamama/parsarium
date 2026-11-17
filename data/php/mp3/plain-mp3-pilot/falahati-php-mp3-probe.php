<?php
// Lead check for falahati/php-mp3; not a selected or runnable Parsarium path.
// Usage: php -d error_reporting=0 falahati-php-mp3-probe.php <package root> <control.mp3>
require $argv[1] . '/src/MpegAudioFrameHeader.php';
require $argv[1] . '/src/MpegAudio.php';

$audio = \falahati\PHPMP3\MpegAudio::fromFile($argv[2]);
$frames = $audio->getFrameCounts();
$out = ['frames' => $frames, 'duration' => $audio->getTotalDuration()];
$first = $audio->getFrameHeader(0);
if ($first !== false) {
    foreach (['getVersion', 'getLayerProfile', 'getSampleRate', 'getBitRate',
              'getChannelMode', 'getOffset', 'getLength'] as $method) {
        $out[$method] = $first->$method();
    }
}
$out['frame_offsets'] = [];
for ($i = 0; $i < $frames; $i++) {
    $out['frame_offsets'][] = $audio->getFrameHeader($i)->getOffset();
}
echo json_encode($out), "\n";
