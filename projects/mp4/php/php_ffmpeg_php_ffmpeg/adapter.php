<?php
declare(strict_types=1);

[$script, $package, $path] = $argv + [null, null, null];
if ($package === null || $path === null) {
    throw new InvalidArgumentException('usage: php parse.php PACKAGE CONTROL');
}

$vendor = match ($package) {
    'james-heinrich/getid3', 'owen-oj/laravel-getid3' => '/mp3/vendor/autoload.php',
    'mhor/php-mediainfo' => '/mp3/mediainfo/vendor/autoload.php',
    'buggedcom/phpvideotoolkit' => '/mp3/phptoolkit/vendor/autoload.php',
    'php-ffmpeg/php-ffmpeg' => '/wav/php_ffmpeg/vendor/autoload.php',
    'sempia/getid3' => '/mp3/sempia/vendor/autoload.php',
    'wikimedia/getid3' => '/mp3/wikimedia/vendor/autoload.php',
    'indiehd/audio-manipulator' => '/mp3/indiehd/vendor/autoload.php',
    'audiostreamify/hvap' => '/mp3/hvap/vendor/autoload.php',
    'nicoverbruggen/mediaprobe' => '/mp3/mediaprobe/vendor/autoload.php',
    'soluble/mediatools' => '/wav/soluble/vendor/autoload.php',
    'rasuvaeff/media-converter' => '/wav/rasuvaeff/vendor/autoload.php',
    'protonemedia/php-ffmpeg' => '/wav/protonemedia/vendor/autoload.php',
    'char0n/ffmpeg-php' => '/wav/char0n/vendor/autoload.php',
    'uberchel/mediainfo4php' => '/wav/uberchel/vendor/autoload.php',
    'clwu/php-read-mp4info' => '/mp4/clwu/vendor/autoload.php',
    'aminyazdanpanah/php-ffmpeg-video-streaming' => '/mp4/aminyaz/vendor/autoload.php',
    'fmonts/ffmpeg-bundle' => '/mp4/fmonts/vendor/autoload.php',
    'minuteoflaravel/laravel-audio-video-validator' => '/mp4/minute/vendor/autoload.php',
    'kiwilan/php-audio' => '/mp3/kiwilan/vendor/autoload.php',
    default => throw new InvalidArgumentException('unknown MP4 package: ' . $package),
};
    require __DIR__ . '/vendor/autoload.php';

switch ($package) {
    case 'james-heinrich/getid3':
        $parsed = (new \getID3())->analyze($path);
        $output = [
            'format' => $parsed['fileformat'] ?? null,
            'width' => $parsed['video']['resolution_x'] ?? null,
            'height' => $parsed['video']['resolution_y'] ?? null,
            'video_fourcc' => $parsed['video']['fourcc'] ?? null,
            'audio_channels' => $parsed['audio']['channels'] ?? null,
        ];
        break;
    case 'owen-oj/laravel-getid3':
        $parsed = (new \Owenoj\LaravelGetId3\GetId3($path))->extractInfo();
        $output = [
            'format' => $parsed['fileformat'] ?? null,
            'width' => $parsed['video']['resolution_x'] ?? null,
            'height' => $parsed['video']['resolution_y'] ?? null,
            'video_fourcc' => $parsed['video']['fourcc'] ?? null,
        ];
        break;
    case 'mhor/php-mediainfo':
        $video = (new \Mhor\MediaInfo\MediaInfo())->getInfo($path)->getVideos()[0] ?? null;
        $output = [
            'video_format' => $video?->get('format')?->getShortName(),
            'width' => $video?->get('width')?->getAbsoluteValue(),
            'height' => $video?->get('height')?->getAbsoluteValue(),
        ];
        break;
    case 'buggedcom/phpvideotoolkit':
        $parsed = (new \PHPVideoToolkit\MediaParser())->getFileInformation($path);
        $output = [
            'container' => $parsed['container'] ?? null,
            'video_codec' => $parsed['video']['codec']['name'] ?? null,
            'width' => $parsed['video']['dimensions']['width'] ?? null,
            'height' => $parsed['video']['dimensions']['height'] ?? null,
        ];
        break;
    case 'php-ffmpeg/php-ffmpeg':
    case 'protonemedia/php-ffmpeg':
        $video = \FFMpeg\FFProbe::create()->streams($path)->videos()->first();
        $output = [
            'video_codec' => $video?->get('codec_name'),
            'width' => $video?->get('width'),
            'height' => $video?->get('height'),
            'video_fourcc' => $video?->get('codec_tag_string'),
        ];
        break;
    case 'sempia/getid3':
    case 'wikimedia/getid3':
        $parsed = (new \JamesHeinrich\GetID3\GetID3())->analyze($path);
        $output = [
            'format' => $parsed['fileformat'] ?? null,
            'width' => $parsed['video']['resolution_x'] ?? null,
            'height' => $parsed['video']['resolution_y'] ?? null,
            'video_fourcc' => $parsed['video']['fourcc'] ?? null,
        ];
        break;
    case 'indiehd/audio-manipulator':
        $parsed = (new \IndieHD\AudioManipulator\MediaParsing\MediaParser())->analyze($path);
        $output = [
            'format' => $parsed['fileformat'] ?? null,
            'width' => $parsed['video']['resolution_x'] ?? null,
            'height' => $parsed['video']['resolution_y'] ?? null,
            'video_fourcc' => $parsed['video']['fourcc'] ?? null,
        ];
        break;
    case 'audiostreamify/hvap':
        $parsed = \Audiostreamify\Hvap\Processor::audio($path)->analyze();
        $output = [
            'format' => $parsed['fileformat'] ?? null,
            'width' => $parsed['video']['resolution_x'] ?? null,
            'height' => $parsed['video']['resolution_y'] ?? null,
            'video_fourcc' => $parsed['video']['fourcc'] ?? null,
        ];
        break;
    case 'nicoverbruggen/mediaprobe':
        $parsed = (new \NicoVerbruggen\MediaProbe\MediaProbe($path))->getMediaInfo();
        $output = [
            'container' => $parsed->format->format_name ?? null,
            'streams' => $parsed->format->nb_streams ?? null,
            'title' => $parsed->format->tags->title ?? null,
        ];
        break;
    case 'soluble/mediatools':
        $parsed = (new \Soluble\MediaTools\Video\VideoInfoReader(
            new \Soluble\MediaTools\Video\Config\FFProbeConfig('ffprobe')
        ))->getInfo($path);
        $video = $parsed->getVideoStreams()->getFirst();
        $output = [
            'container' => $parsed->getFormatName(),
            'video_codec' => $video->getCodecName(),
            'width' => $video->getWidth(),
            'height' => $video->getHeight(),
        ];
        break;
    case 'rasuvaeff/media-converter':
        $parsed = (new \Rasuvaeff\MediaConverter\FfprobeMediaInfo(
            new \Rasuvaeff\MediaConverter\FfmpegBinary('ffmpeg', 'ffprobe'),
            new \Rasuvaeff\MediaConverter\SymfonyProcessRunner()
        ))->probe($path);
        $output = [
            'video_codec' => $parsed->videoCodec(),
            'width' => $parsed->width(),
            'height' => $parsed->height(),
            'duration_seconds' => $parsed->duration()->toSeconds(),
        ];
        break;
    case 'char0n/ffmpeg-php':
        $parsed = new \Char0n\FFMpegPHP\Movie($path);
        $output = [
            'video_codec' => explode(' ', $parsed->getVideoCodec())[0],
            'duration_seconds' => $parsed->getDuration(),
        ];
        break;
    case 'uberchel/mediainfo4php':
        $parsed = \uberchel\MediaInfo::Get($path, false);
        $output = [
            'video_codec' => $parsed['streams']['video']['codec'] ?? null,
            'width' => (int) ($parsed['streams']['video']['width'] ?? 0),
            'height' => (int) ($parsed['streams']['video']['height'] ?? 0),
            'title' => $parsed['title'] ?? null,
        ];
        break;
    case 'clwu/php-read-mp4info':
        $parsed = \Clwu\Mp4::getInfo($path);
        $output = [
            'width' => $parsed['width'] ?? null,
            'height' => $parsed['height'] ?? null,
            'rotate' => $parsed['rotate'] ?? null,
        ];
        break;
    case 'aminyazdanpanah/php-ffmpeg-video-streaming':
        $video = \Streaming\FFMpeg::create()->open($path)->getStreams()->videos()->first();
        $output = [
            'video_codec' => $video?->get('codec_name'),
            'width' => $video?->get('width'),
            'height' => $video?->get('height'),
        ];
        break;
    case 'fmonts/ffmpeg-bundle':
        $container = new \Symfony\Component\DependencyInjection\ContainerBuilder();
        $container->register('logger', \Psr\Log\NullLogger::class)->setPublic(true);
        (new \Dubture\FFmpegBundle\DependencyInjection\DubtureFFmpegExtension())->load([[
            'ffmpeg_binary' => getenv('PARSARIUM_FFMPEG') ?: '/opt/homebrew/bin/ffmpeg',
            'ffprobe_binary' => getenv('PARSARIUM_FFPROBE') ?: '/opt/homebrew/bin/ffprobe',
            'temporary_directory' => sys_get_temp_dir(),
        ]], $container);
        $container->getDefinition('dubture_ffmpeg.ffprobe')->setPublic(true);
        $container->compile();
        $video = $container->get('dubture_ffmpeg.ffprobe')->streams($path)->videos()->first();
        $output = [
            'video_codec' => $video?->get('codec_name'),
            'width' => $video?->get('width'),
            'height' => $video?->get('height'),
        ];
        break;
    case 'minuteoflaravel/laravel-audio-video-validator':
        $validator = new \MinuteOfLaravel\MediaValidator\MediaValidator();
        $isVideo = $validator->validateVideo('file', $path);
        $video = $validator->getVideoStream();
        $output = [
            'is_video' => $isVideo,
            'video_codec' => $video?->get('codec_name'),
            'width' => $video?->get('width'),
            'height' => $video?->get('height'),
        ];
        break;
    case 'kiwilan/php-audio':
        $parsed = \Kiwilan\Audio\Audio::read($path)->getMetadata();
        $output = [
            'format' => $parsed->getDataFormat(),
            'audio_sample_rate' => $parsed->getSampleRate(),
            'audio_channels' => $parsed->getChannels(),
            'audio_codec' => $parsed->getCodec(),
        ];
        break;
}

echo json_encode($output, JSON_THROW_ON_ERROR), "\n";
