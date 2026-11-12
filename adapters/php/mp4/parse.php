<?php
declare(strict_types=1);

[$script, $package, $path] = $argv + [null, null, null];
if ($package === null || $path === null) {
    throw new InvalidArgumentException('usage: php parse.php PACKAGE CONTROL');
}

$vendor = match ($package) {
    'james-heinrich/getid3', 'owen-oj/laravel-getid3' => '/mp3_id3v2/vendor/autoload.php',
    'mhor/php-mediainfo' => '/mp3_id3v2/mediainfo/vendor/autoload.php',
    'buggedcom/phpvideotoolkit' => '/mp3_id3v2/phptoolkit/vendor/autoload.php',
    'php-ffmpeg/php-ffmpeg' => '/wav/php_ffmpeg/vendor/autoload.php',
    default => throw new InvalidArgumentException('unknown MP4 package: ' . $package),
};
require dirname(__DIR__) . $vendor;

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
        $video = (new \Mhor\MediaInfo\MediaInfo())->getInfo($path)->getVideos()[0];
        $output = [
            'video_format' => $video->get('format')->getShortName(),
            'width' => $video->get('width')->getAbsoluteValue(),
            'height' => $video->get('height')->getAbsoluteValue(),
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
        $video = \FFMpeg\FFProbe::create()->streams($path)->videos()->first();
        $output = [
            'video_codec' => $video->get('codec_name'),
            'width' => $video->get('width'),
            'height' => $video->get('height'),
            'video_fourcc' => $video->get('codec_tag_string'),
        ];
        break;
}

echo json_encode($output, JSON_THROW_ON_ERROR), "\n";
