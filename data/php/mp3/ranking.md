# PHP plain MP3 parser pilot

The only verified third-party path in this pilot is
[`james-heinrich/getid3`](../../../projects/mp3/php/getid3/README.md) v1.9.28.
Its `getID3::analyze()` file API ran `module.audio.mp3.php` on both untagged
MPEG Layer III controls: it found no tag, read the first frame header, checked
frame sync, and reported version, layer, sample rate, channels, bitrate and
frame length. The package has **15,766,894 Packagist downloads** in the
[saved search snapshot](registry-snapshot.json). That counts Composer installs
of the whole package, including installs pulled in by wrappers; it is an
adoption proxy, not a count of programs that read MP3 frames. getID3 is already
counted in the active PHP MP3-with-ID3v2 cell. This is a separate plain-frame
path in the same parser family.

## Primary within-cell adoption metric

Packagist total downloads, captured 2026-11-17.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [james-heinrich/getid3](https://github.com/JamesHeinrich/getID3/blob/v1.9.28/README.md) | v1.9.28 | 15,766,894 | First MPEG frame header with frame-sync check: version, layer, sample rate, channels, bitrate, frame length; CBR duration from audio bytes and header bitrate | getID3 native MP3 frame parser |

On the 44.1 kHz mono control it reports MPEG-1 Layer III, 64 kbit/s CBR,
208-byte frames and 0.28725 s. On the 22.05 kHz stereo control it reports
MPEG-2 Layer III joint stereo, 32 kbit/s, 104-byte frames and 0.3135 s. The
duration is header bitrate times audio-data length, not a frame count; getID3
does not decode audio here.

## Leads

Seven Packagist queries returned 100 hits and 79 distinct packages. The
[leads](leads.json) record each one. None of these is a verified entry.

- wapmorgan/mp3info (1,512,916): an independent PHP frame-header reader;
  unresolved, not run on the plain controls.
- falahati/php-mp3 (80,144) and its copy holine/mp3: native PHP MPEG audio
  reader; unresolved.
- debach/zend-mp3 (45,227) and fobilow/mp3file (5,468): unresolved.
- buggedcom/phpvideotoolkit, nicoverbruggen/mediaprobe and phpmlkit/soundfile
  hand parsing to FFmpeg or libsndfile; unresolved native paths.
- 19 getID3 forks and wrappers (for example owen-oj/laravel-getid3 and
  kiwilan/php-audio) share the selected family.
- 48 hits are excluded: tag-only readers, encoder wrappers, converters,
  downloaders and unrelated packages.

This one-entry pilot is neither a top-ten ranking nor evidence that only one
PHP frame parser exists. The [cell record](cell.json) gives the remaining
uncertainty and the [PHP runtime finding](standard.json).
