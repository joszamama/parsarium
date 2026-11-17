<?php
declare(strict_types=1);

[$script, $package, $path] = $argv + [null, null, null];
if ($package === null || $path === null) {
    throw new InvalidArgumentException('usage: php parse.php PACKAGE CONTROL');
}

$vendor = match ($package) {
    'james-heinrich/getid3' => '/mp3/vendor/autoload.php',
    'mhor/php-mediainfo' => '/mp3/mediainfo/vendor/autoload.php',
    'buggedcom/phpvideotoolkit' => '/mp3/phptoolkit/vendor/autoload.php',
    'phpmlkit/soundfile' => '/mp3/soundfile/vendor/autoload.php',
    'owen-oj/laravel-getid3' => '/mp3/vendor/autoload.php',
    'sempia/getid3' => '/mp3/sempia/vendor/autoload.php',
    'wikimedia/getid3' => '/mp3/wikimedia/vendor/autoload.php',
    'indiehd/audio-manipulator' => '/mp3/indiehd/vendor/autoload.php',
    'audiostreamify/hvap' => '/mp3/hvap/vendor/autoload.php',
    'kiwilan/php-audio' => '/mp3/kiwilan/vendor/autoload.php',
    'nicoverbruggen/mediaprobe' => '/mp3/mediaprobe/vendor/autoload.php',
    'php-ffmpeg/php-ffmpeg' => '/wav/php_ffmpeg/vendor/autoload.php',
    'gemorroj/file-wav' => '/wav/file_wav/vendor/autoload.php',
    'soluble/mediatools' => '/wav/soluble/vendor/autoload.php',
    'rasuvaeff/media-converter' => '/wav/rasuvaeff/vendor/autoload.php',
    'protonemedia/php-ffmpeg' => '/wav/protonemedia/vendor/autoload.php',
    'maximal/audio-waveform' => '/wav/maximal/vendor/autoload.php',
    'char0n/ffmpeg-php' => '/wav/char0n/vendor/autoload.php',
    'uberchel/mediainfo4php' => '/wav/uberchel/vendor/autoload.php',
    'bpmfinder/bpm-finder' => '/wav/bpmfinder/vendor/autoload.php',
    default => throw new InvalidArgumentException('unknown WAV package: ' . $package),
};
    require __DIR__ . '/vendor/autoload.php';

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
    case 'php-ffmpeg/php-ffmpeg':
    case 'protonemedia/php-ffmpeg':
        $parsed = \FFMpeg\FFProbe::create()->streams($path)->audios()->first();
        $output = [
            'codec' => $parsed->get('codec_name'),
            'sample_rate' => $parsed->get('sample_rate'),
            'channels' => $parsed->get('channels'),
            'bits_per_sample' => $parsed->get('bits_per_sample'),
        ];
        break;
    case 'gemorroj/file-wav':
        $parsed = (new \FileWav\Wav($path))->getInfo();
        $output = [
            'compression' => $parsed->getCompression(),
            'sample_rate' => $parsed->getFramerate(),
            'channels' => $parsed->getChannels(),
            'bits_per_sample' => $parsed->getBits(),
            'duration_seconds' => $parsed->getLength(),
        ];
        break;
    case 'soluble/mediatools':
        $parsed = (new \Soluble\MediaTools\Video\VideoInfoReader(
            new \Soluble\MediaTools\Video\Config\FFProbeConfig('ffprobe')
        ))->getInfo($path);
        $output = [
            'format' => $parsed->getFormatName(),
            'duration_seconds' => $parsed->getDuration(),
            'audio_codec' => $parsed->getAudioStreams()->getFirst()->getCodecName(),
        ];
        break;
    case 'rasuvaeff/media-converter':
        $parsed = (new \Rasuvaeff\MediaConverter\FfprobeMediaInfo(
            new \Rasuvaeff\MediaConverter\FfmpegBinary('ffmpeg', 'ffprobe'),
            new \Rasuvaeff\MediaConverter\SymfonyProcessRunner()
        ))->probe($path);
        $output = [
            'audio_codec' => $parsed->audioCodec(),
            'duration_seconds' => $parsed->duration()->toSeconds(),
            'bit_rate' => $parsed->bitrate(),
        ];
        break;
    case 'maximal/audio-waveform':
        $parsed = (new \maximal\audio\Waveform($path))->getWaveformData(8);
        $output = [
            'first_channel_samples' => count($parsed['lines1']),
            'second_channel_samples' => count($parsed['lines2']),
            'has_positive_amplitude' => max($parsed['lines1']) > 0,
            'has_negative_amplitude' => min($parsed['lines1']) < 0,
        ];
        break;
    case 'char0n/ffmpeg-php':
        $parsed = new \Char0n\FFMpegPHP\Movie($path);
        $output = [
            'audio_codec' => explode(' ', $parsed->getAudioCodec())[0],
            'sample_rate' => $parsed->getAudioSampleRate(),
            'channels' => $parsed->getAudioChannels(),
            'duration_seconds' => $parsed->getDuration(),
        ];
        break;
    case 'uberchel/mediainfo4php':
        $parsed = \uberchel\MediaInfo::Get($path, false);
        $audio = $parsed['streams']['audios'][0];
        $output = [
            'audio_codec' => explode(' ', $audio['codec'])[0],
            'sample_rate' => $audio['rates'],
            'channels' => $audio['channels'],
            'bit_rate' => $audio['bitrate'],
        ];
        break;
    case 'bpmfinder/bpm-finder':
        $parsed = \BpmFinder\TempoTools\AudioFileBpmAnalyzer::analyzeFile($path);
        $output = [
            'format' => $parsed['format'],
            'sample_rate' => $parsed['sample_rate'],
            'channels' => $parsed['channels'],
            'duration_seconds' => $parsed['duration_seconds'],
            'bpm' => $parsed['bpm'],
        ];
        break;
}

echo json_encode($output, JSON_THROW_ON_ERROR), "\n";
