<?php
declare(strict_types=1);

[$script, $package, $path] = $argv + [null, null, null];
if ($package === null || $path === null) {
    throw new InvalidArgumentException('usage: php parse.php PACKAGE CONTROL');
}

$vendor = match ($package) {
    'wapmorgan/media-file' => '/legacy/vendor/autoload.php',
    'kiwilan/php-audio' => '/kiwilan/vendor/autoload.php',
    'duncan3dc/meta-audio' => '/meta_audio/vendor/autoload.php',
    'debach/zend-mp3' => '/zend_mp3/vendor/autoload.php',
    'mhor/php-mediainfo' => '/mediainfo/vendor/autoload.php',
    'buggedcom/phpvideotoolkit' => '/phptoolkit/vendor/autoload.php',
    'vollbehr/php-reader' => '/vollbehr/vendor/autoload.php',
    'pyrex-fwi/id3' => '/pyrex/vendor/autoload.php',
    'sempia/getid3' => '/sempia/vendor/autoload.php',
    'indiehd/audio-manipulator' => '/indiehd/vendor/autoload.php',
    'wikimedia/getid3' => '/wikimedia/vendor/autoload.php',
    'nicoverbruggen/mediaprobe' => '/mediaprobe/vendor/autoload.php',
    'dgoriaev/mp3info' => '/dgoriaev/vendor/autoload.php',
    'codememory/media-file-fork' => '/codememory/vendor/autoload.php',
    'phpmlkit/soundfile' => '/soundfile/vendor/autoload.php',
    'audiostreamify/hvap' => '/hvap/vendor/autoload.php',
    default => '/vendor/autoload.php',
};
    require __DIR__ . '/vendor/autoload.php';

switch ($package) {
    case 'james-heinrich/getid3':
        $parsed = (new \getID3())->analyze($path);
        $tags = $parsed['tags']['id3v2'] ?? [];
        $output = [
            'title' => $tags['title'][0] ?? null,
            'artist' => $tags['artist'][0] ?? null,
            'album' => $tags['album'][0] ?? null,
            'id3v2_major' => $parsed['id3v2']['majorversion'] ?? null,
        ];
        break;
    case 'wapmorgan/mp3info':
        $parsed = new \wapmorgan\Mp3Info\Mp3Info($path, true);
        $output = [
            'title' => $parsed->tags2['TIT2'] ?? null,
            'artist' => $parsed->tags2['TPE1'] ?? null,
            'album' => $parsed->tags2['TALB'] ?? null,
            'id3v2_major' => $parsed->id3v2MajorVersion ?? null,
        ];
        break;
    case 'christophwurst/id3parser':
        $parsed = (new \ID3Parser\ID3Parser())->analyze($path);
        $tags = $parsed['id3v2']['comments'] ?? [];
        $output = [
            'title' => $tags['title'][0] ?? null,
            'artist' => $tags['artist'][0] ?? null,
            'album' => $tags['album'][0] ?? null,
            'id3v2_major' => $parsed['id3v2']['majorversion'] ?? null,
        ];
        break;
    case 'owen-oj/laravel-getid3':
        $parsed = new \Owenoj\LaravelGetId3\GetId3($path);
        $info = $parsed->extractInfo();
        $output = [
            'title' => $parsed->getTitle(),
            'artist' => $parsed->getArtist(),
            'album' => $parsed->getAlbum(),
            'id3v2_major' => $info['id3v2']['majorversion'] ?? null,
        ];
        break;
    case 'wapmorgan/media-file':
        $parsed = \wapmorgan\MediaFile\MediaFile::open($path);
        $output = [
            'is_audio' => $parsed->isAudio(),
            'sample_rate' => $parsed->getAudio()->getSampleRate(),
            'bit_rate' => $parsed->getAudio()->getBitRate(),
        ];
        break;
    case 'kiwilan/php-audio':
        $parsed = \Kiwilan\Audio\Audio::read($path);
        $output = [
            'title' => $parsed->getTitle(),
            'artist' => $parsed->getArtist(),
            'album' => $parsed->getAlbum(),
        ];
        break;
    case 'duncan3dc/meta-audio':
        $tagger = new \duncan3dc\MetaAudio\Tagger();
        $tagger->addDefaultModules();
        $parsed = $tagger->open($path);
        $output = [
            'title' => $parsed->getTitle(),
            'artist' => $parsed->getArtist(),
            'album' => $parsed->getAlbum(),
        ];
        break;
    case 'debach/zend-mp3':
        $parsed = new \Zend_Media_Id3v2($path);
        $output = [];
        foreach (['title' => 'TIT2', 'artist' => 'TPE1', 'album' => 'TALB'] as $field => $frameId) {
            $frames = $parsed->getFramesByIdentifier($frameId);
            $output[$field] = $frames[0]->getText();
        }
        break;
    case 'mhor/php-mediainfo':
        $general = (new \Mhor\MediaInfo\MediaInfo())->getInfo($path)->getGeneral();
        $output = [
            'title' => $general->get('title'),
            'artist' => $general->get('performer'),
            'album' => $general->get('album'),
        ];
        break;
    case 'buggedcom/phpvideotoolkit':
        $parsed = (new \PHPVideoToolkit\MediaParser())->getFileInformation($path);
        $output = [
            'title' => $parsed['metadata']['title'] ?? null,
            'artist' => $parsed['metadata']['artist'] ?? null,
            'album' => $parsed['metadata']['album'] ?? null,
            'sample_rate' => $parsed['audio']['sample']['rate'] ?? null,
            'codec' => $parsed['audio']['codec']['name'] ?? null,
        ];
        break;
    case 'vollbehr/php-reader':
        $parsed = new \Vollbehr\Media\Id3v2(new \Vollbehr\Io\FileReader($path));
        $output = [];
        foreach (['title' => 'TIT2', 'artist' => 'TPE1', 'album' => 'TALB'] as $field => $frameId) {
            $frames = $parsed->getFramesByIdentifier($frameId);
            $output[$field] = $frames[0]->getText();
        }
        break;
    case 'pyrex-fwi/id3':
        $parsed = new \Cpyree\Id3\Metadata\Id3Metadata($path);
        $reader = new \Cpyree\Id3\Wrapper\BinWrapper\MediainfoWrapper();
        $reader->setBinPath(__DIR__ . '/pyrex/mediainfo_oldxml.sh');
        if (!$reader->read($parsed)) {
            throw new RuntimeException('Pyrex MediaInfo wrapper did not parse the tagged MP3');
        }
        $output = [
            'title' => $parsed->getTitle(),
            'artist' => $parsed->getArtist(),
            'album' => $parsed->getAlbum(),
        ];
        break;
    case 'sempia/getid3':
        $parsed = (new \JamesHeinrich\GetID3\GetID3())->analyze($path);
        $tags = $parsed['tags']['id3v2'] ?? [];
        $output = [
            'title' => $tags['title'][0] ?? null,
            'artist' => $tags['artist'][0] ?? null,
            'album' => $tags['album'][0] ?? null,
            'id3v2_major' => $parsed['id3v2']['majorversion'] ?? null,
        ];
        break;
    case 'indiehd/audio-manipulator':
        $parsed = (new \IndieHD\AudioManipulator\MediaParsing\MediaParser())->analyze($path);
        $tags = $parsed['tags']['id3v2'] ?? [];
        $output = [
            'title' => $tags['title'][0] ?? null,
            'artist' => $tags['artist'][0] ?? null,
            'album' => $tags['album'][0] ?? null,
            'id3v2_major' => $parsed['id3v2']['majorversion'] ?? null,
        ];
        break;
    case 'wikimedia/getid3':
        $parsed = (new \JamesHeinrich\GetID3\GetID3())->analyze($path);
        $tags = $parsed['tags']['id3v2'] ?? [];
        $output = [
            'title' => $tags['title'][0] ?? null,
            'artist' => $tags['artist'][0] ?? null,
            'album' => $tags['album'][0] ?? null,
            'id3v2_major' => $parsed['id3v2']['majorversion'] ?? null,
        ];
        break;
    case 'nicoverbruggen/mediaprobe':
        $parsed = (new \NicoVerbruggen\MediaProbe\MediaProbe($path))->getMediaInfo();
        $output = [
            'title' => $parsed->format->tags->title ?? null,
            'artist' => $parsed->format->tags->artist ?? null,
            'album' => $parsed->format->tags->album ?? null,
        ];
        break;
    case 'dgoriaev/mp3info':
        $parsed = new \dgoriaev\Mp3Info\Mp3Info($path, true);
        $output = [
            'title' => $parsed->tags2['TIT2'] ?? null,
            'artist' => $parsed->tags2['TPE1'] ?? null,
            'album' => $parsed->tags2['TALB'] ?? null,
            'id3v2_major' => $parsed->id3v2MajorVersion ?? null,
        ];
        break;
    case 'codememory/media-file-fork':
        $parsed = \wapmorgan\MediaFile\MediaFile::open($path);
        $output = [
            'is_audio' => $parsed->isAudio(),
            'sample_rate' => $parsed->getAudio()->getSampleRate(),
            'bit_rate' => $parsed->getAudio()->getBitRate(),
        ];
        break;
    case 'phpmlkit/soundfile':
        $info = \PhpMlKit\SoundFile\sf_info($path);
        $tags = \PhpMlKit\SoundFile\sf_metadata($path);
        $output = [
            'title' => $tags->title,
            'artist' => $tags->artist,
            'album' => $tags->album,
            'sample_rate' => $info->sampleRate,
            'format' => $info->format->name,
            'subtype' => $info->sampleFormat->name,
        ];
        break;
    case 'audiostreamify/hvap':
        $parsed = \Audiostreamify\Hvap\Processor::audio($path)->analyze();
        $tags = $parsed['tags']['id3v2'] ?? [];
        $output = [
            'title' => $tags['title'][0] ?? null,
            'artist' => $tags['artist'][0] ?? null,
            'album' => $tags['album'][0] ?? null,
            'id3v2_major' => $parsed['id3v2']['majorversion'] ?? null,
        ];
        break;
    default:
        throw new InvalidArgumentException('unknown MP3/ID3v2 package: ' . $package);
}

echo json_encode($output, JSON_THROW_ON_ERROR), "\n";
