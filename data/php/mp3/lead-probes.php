<?php
// Lead checks for the PHP plain MP3 cell; none of these is a selected or runnable Parsarium path.
// Usage: php lead-probes.php <zend|mp3file|flv2mp4> <package root> <control.mp3>...
// Only the documented valid controls in controls/mp3/ were used.
[$mode, $root] = [$argv[1], $argv[2]];
$controls = array_slice($argv, 3);

if ($mode === 'zend') {
    // debach/zend-mp3 1.8.1: README "Reading the duration of an MP3 file" API.
    set_include_path($root . '/lib');
    spl_autoload_register(static function (string $class): void {
        require str_replace('_', '/', $class) . '.php';
    });
    foreach ($controls as $control) {
        $abs = new Zend_Media_Mpeg_Abs($control);
        $frames = $abs->getFrames();
        echo basename($control), ' ', json_encode(['frames' => count($frames),
            'sample_rate' => $frames[0]->getSamplingFrequency(), 'mode' => $frames[0]->getMode(),
            'bitrate' => $frames[0]->getBitrate(), 'length' => $abs->getLength()]), "\n";
    }
} elseif ($mode === 'mp3file') {
    // fobilow/mp3file dev-master: README constructor and get_metadata().
    require $root . '/Mp3File.php';
    foreach ($controls as $control) {
        echo basename($control), ' ', json_encode((new Mp3File($control))->get_metadata()), "\n";
    }
} elseif ($mode === 'flv2mp4') {
    // xiaosongshu/flv2mp4 v1.8.7: the in-process decoder behind Manage\Mp32Pcm.
    spl_autoload_register(static function (string $class) use ($root): void {
        $prefix = 'Xiaosongshu\\Flv2mp4\\';
        if (str_starts_with($class, $prefix)) {
            require $root . '/src/' . str_replace('\\', '/', substr($class, strlen($prefix))) . '.php';
        }
    });
    foreach ($controls as $control) {
        $decoded = (new Xiaosongshu\Flv2mp4\Mp3\Mp3L3Decoder())->decode(file_get_contents($control));
        echo basename($control), ' ', json_encode(['sampleRate' => $decoded['sampleRate'],
            'channels' => $decoded['channels'], 'samples_per_channel' => array_map('count', $decoded['planes'])]), "\n";
    }
} else {
    fwrite(STDERR, "unknown mode\n");
    exit(2);
}
