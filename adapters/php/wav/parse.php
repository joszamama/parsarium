<?php
declare(strict_types=1);

[$script, $package, $path] = $argv + [null, null, null];
if ($package === null || $path === null) {
    throw new InvalidArgumentException('usage: php parse.php PACKAGE CONTROL');
}

$vendor = match ($package) {
    'james-heinrich/getid3' => '/mp3_id3v2/vendor/autoload.php',
    'mhor/php-mediainfo' => '/mp3_id3v2/mediainfo/vendor/autoload.php',
    'buggedcom/phpvideotoolkit' => '/mp3_id3v2/phptoolkit/vendor/autoload.php',
    'phpmlkit/soundfile' => '/mp3_id3v2/soundfile/vendor/autoload.php',
    'owen-oj/laravel-getid3' => '/mp3_id3v2/vendor/autoload.php',
    'sempia/getid3' => '/mp3_id3v2/sempia/vendor/autoload.php',
    'wikimedia/getid3' => '/mp3_id3v2/wikimedia/vendor/autoload.php',
    'indiehd/audio-manipulator' => '/mp3_id3v2/indiehd/vendor/autoload.php',
    'audiostreamify/hvap' => '/mp3_id3v2/hvap/vendor/autoload.php',
    'kiwilan/php-audio' => '/mp3_id3v2/kiwilan/vendor/autoload.php',
    'nicoverbruggen/mediaprobe' => '/mp3_id3v2/mediaprobe/vendor/autoload.php',
    default => throw new InvalidArgumentException('unknown WAV package: ' . $package),
};
require dirname(__DIR__) . $vendor;

switch ($package) {
    case 'james-heinrich/getid3':
        $parsed = (new \getID3())->analyze($path);
        $output = [
            'fileformat' => $parsed['fileformat'] ?? null,
            'sample_rate' => $parsed['audio']['sample_rate'] ?? null,
            'channels' => $parsed['audio']['channels'] ?? null,
            'bits_per_sample' => $parsed['audio']['bits_per_sample'] ?? null,
        ];
        break;
    case 'mhor/php-mediainfo':
        $parsed = (new \Mhor\MediaInfo\MediaInfo())->getInfo($path)->getAudios()[0];
        $output = [
            'format' => $parsed->get('format')->getShortName(),
            'sample_rate' => $parsed->get('sampling_rate')->getAbsoluteValue(),
            'channels' => $parsed->get('channel_s')->getAbsoluteValue(),
            'bit_depth' => $parsed->get('bit_depth')->getAbsoluteValue(),
        ];
        break;
    case 'buggedcom/phpvideotoolkit':
        $parsed = (new \PHPVideoToolkit\MediaParser())->getFileInformation($path);
        $output = [
            'sample_rate' => $parsed['audio']['sample']['rate'] ?? null,
            'channels' => $parsed['audio']['channels'] ?? null,
            'codec' => $parsed['audio']['codec']['name'] ?? null,
        ];
        break;
    case 'phpmlkit/soundfile':
        $parsed = \PhpMlKit\SoundFile\sf_info($path);
        $output = [
            'sample_rate' => $parsed->sampleRate,
            'channels' => $parsed->channels,
            'format' => $parsed->format->name,
            'subtype' => $parsed->sampleFormat->name,
        ];
        break;
    case 'owen-oj/laravel-getid3':
        $parsed = (new \Owenoj\LaravelGetId3\GetId3($path))->extractInfo();
        $output = [
            'fileformat' => $parsed['fileformat'] ?? null,
            'sample_rate' => $parsed['audio']['sample_rate'] ?? null,
            'channels' => $parsed['audio']['channels'] ?? null,
            'bits_per_sample' => $parsed['audio']['bits_per_sample'] ?? null,
        ];
        break;
    case 'sempia/getid3':
    case 'wikimedia/getid3':
        $parsed = (new \JamesHeinrich\GetID3\GetID3())->analyze($path);
        $output = [
            'fileformat' => $parsed['fileformat'] ?? null,
            'sample_rate' => $parsed['audio']['sample_rate'] ?? null,
            'channels' => $parsed['audio']['channels'] ?? null,
            'bits_per_sample' => $parsed['audio']['bits_per_sample'] ?? null,
        ];
        break;
    case 'indiehd/audio-manipulator':
        $parsed = (new \IndieHD\AudioManipulator\MediaParsing\MediaParser())->analyze($path);
        $output = [
            'fileformat' => $parsed['fileformat'] ?? null,
            'sample_rate' => $parsed['audio']['sample_rate'] ?? null,
            'channels' => $parsed['audio']['channels'] ?? null,
            'bits_per_sample' => $parsed['audio']['bits_per_sample'] ?? null,
        ];
        break;
    case 'audiostreamify/hvap':
        $parsed = \Audiostreamify\Hvap\Processor::audio($path)->analyze();
        $output = [
            'fileformat' => $parsed['fileformat'] ?? null,
            'sample_rate' => $parsed['audio']['sample_rate'] ?? null,
            'channels' => $parsed['audio']['channels'] ?? null,
            'bits_per_sample' => $parsed['audio']['bits_per_sample'] ?? null,
        ];
        break;
    case 'kiwilan/php-audio':
        $parsed = \Kiwilan\Audio\Audio::read($path)->getMetadata();
        $output = [
            'format' => $parsed->getDataFormat(),
            'sample_rate' => $parsed->getSampleRate(),
            'channels' => $parsed->getChannels(),
            'codec' => $parsed->getCodec(),
        ];
        break;
    case 'nicoverbruggen/mediaprobe':
        $parsed = (new \NicoVerbruggen\MediaProbe\MediaProbe($path))->getMediaInfo();
        $output = [
            'format' => $parsed->format->format_name ?? null,
            'duration_seconds' => $parsed->format->duration ?? null,
            'bit_rate' => $parsed->format->bit_rate ?? null,
        ];
        break;
}

echo json_encode($output, JSON_THROW_ON_ERROR), "\n";
