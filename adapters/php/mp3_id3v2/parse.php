<?php
declare(strict_types=1);

[$script, $package, $path] = $argv + [null, null, null];
if ($package === null || $path === null) {
    throw new InvalidArgumentException('usage: php parse.php PACKAGE CONTROL');
}

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
    default:
        throw new InvalidArgumentException('unknown MP3/ID3v2 package: ' . $package);
}

echo json_encode($output, JSON_THROW_ON_ERROR), "\n";
