# PHP plain MP3 parser pilot

Two third-party paths are verified in this pilot:
[`james-heinrich/getid3`](../../../projects/mp3/php/getid3/README.md) v1.9.28
and [`wapmorgan/mp3info`](../../../projects/mp3/php/wapmorgan_mp3info/README.md)
0.1.1. Both read MPEG Layer III frame headers from untagged input in native PHP.
The download counts in the [saved search snapshot](registry-snapshot.json)
count Composer installs of each whole package, including installs pulled in by
wrappers. They are adoption proxies, not counts of programs that read MP3
frames. getID3 is already counted in the active PHP MP3-with-ID3v2 cell, so its
plain-frame path is in the same parser family. Mp3Info is a separate family: one
class with its own tables and no getID3 code.

## Primary within-cell adoption metric

Packagist total downloads, captured 2026-11-17.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [james-heinrich/getid3](https://github.com/JamesHeinrich/getID3/blob/v1.9.28/README.md) | v1.9.28 | 15,766,894 | First MPEG frame header with frame-sync check: version, layer, sample rate, channels, bitrate, frame length; CBR duration from audio bytes and header bitrate | getID3 native MP3 frame parser |
| 2 | [wapmorgan/mp3info](https://github.com/wapmorgan/Mp3Info/blob/e532c2e1997874f9c672c7810ce90ef15004ef94/README.md) | 0.1.1 | 1,512,916 | MPEG-1 Layer III CBR only: two frame headers (version, layer, sample rate, channel mode, bitrate), frame count from audio bytes and computed frame length | Mp3Info native PHP frame-header reader |

getID3 reports MPEG-1 Layer III, 64 kbit/s CBR, 208-byte frames and 0.28725 s on
the 44.1 kHz mono control. On the 22.05 kHz stereo control it reports MPEG-2
Layer III joint stereo, 32 kbit/s, 104-byte frames and 0.3135 s. Its duration
is header bitrate times audio-data length, not a frame count.

Mp3Info matches the header-walk oracle in `controls/mp3/check_controls.py` on
the 44.1 kHz mono control: MPEG-1 Layer III, mono, 64 kbit/s, 2,298 audio bytes
and 11 frames. It reports 0.26122 s because it computes duration as
(frames - 1) × 1152 / sample rate; the oracle's 11 × 1152 samples are 0.28735 s.
On the 22.05 kHz stereo control it reports MPEG-2 **Layer II, 24 kHz mono,
96 kbit/s, 3 frames** where the oracle reads Layer III, 22.05 kHz stereo,
32 kbit/s and 12 frames. The first header is read correctly. The jump to the
next header uses the MPEG-1 coefficient (208 bytes, not 104), and the two-byte
sync scan skips the real frame at byte 209 and stops on a false sync at byte
236. Its listed scope is therefore MPEG-1 only.

## Leads

Seven Packagist queries returned 100 hits and 79 distinct packages. The
[leads](leads.json) record each one. None of these is a verified entry.

- falahati/php-mp3 (80,144), a separate regin/PHP-MP3 family, failed the
  controls ([audit](falahati-php-mp3-control-audit.md)). The v0.9.5-alpha2 tag
  does not return on PHP 8.5. The dev-master snapshot matches the MPEG-1
  control but reads the MPEG-2 control as 3 frames at 11,025 Hz instead of
  12 frames at 22,050 Hz.
- debach/zend-mp3 1.8.1 (45,227) walks MPEG frames itself in
  `Zend_Media_Mpeg_Abs`, but the parent class file uses `$str{$i}` offsets
  removed in PHP 8. On PHP 8.5 it stops with a parse error on both controls.
  fobilow/mp3file (5,468) has no release tag or license, and it also fails to
  compile. The re-scan found a native MPEG-1 Layer III decoder in
  xiaosongshu/flv2mp4 v1.8.7 (190). It decodes 12,672 samples from the MPEG-1
  control and no frames from the MPEG-2 control, and its documented API
  decodes in a child process. holine/mp3 (9) copies PHP-MP3 and does not
  return on either control. Like falahati/php-mp3, these four are recorded as
  control failures. The [lead audit](lead-audit.md) gives the details.
- wapmorgan/media-file (248,980) builds `Mp3Info` and returns its fields, so it
  is in the same family. dgoriaev/mp3info is an Mp3Info fork.
- buggedcom/phpvideotoolkit, akiosarkiz/mp3php, nicoverbruggen/mediaprobe and
  phpmlkit/soundfile hand parsing to FFmpeg or libsndfile.
- 20 getID3 forks and wrappers share the getID3 family, for example
  owen-oj/laravel-getid3, kiwilan/php-audio and acekyd/laravelmp3, which
  bundles getID3 1.9.5.
- 46 hits are excluded: tag-only readers, encoder wrappers, converters,
  downloaders, unreleased snapshots and unrelated packages.

This two-entry pilot is neither a top-ten ranking nor evidence that only two
PHP frame parsers exist. The [cell record](cell.json) gives the remaining
uncertainty and the [PHP runtime finding](standard.json).
