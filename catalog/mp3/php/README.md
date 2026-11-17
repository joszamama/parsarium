# MP3 / PHP — pilot

**Status:** pilot_two_verified_bounded_search; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Two verified paths; no padding. Search is seven Packagist search.json queries capped at 50 hits each, captured 2026-11-17; package descriptions alone decided most exclusions. Packagist total downloads count Composer installs of the whole package (and wrappers pull getID3 or Mp3Info transitively), not use of the MPEG frame parser. getID3 reads the first frame header, checks sync on following frames, and derives CBR duration from audio-data bytes and the header bitrate. Mp3Info reads two headers, estimates frames from audio bytes and the computed frame length, and reports duration one frame short ((frames - 1) x 1152 / sample rate). On the MPEG-2 control it uses the MPEG-1 frame-length coefficient, misses the third frame and reads a false sync at byte 236, reporting Layer II 24 kHz mono 96 kbit/s; MPEG-2 is not covered for Mp3Info. Neither path decodes audio. PHP-MP3 (falahati/php-mp3) failed the controls: the v0.9.5-alpha2 tag does not return on PHP 8.5, and the dev-master snapshot reads the MPEG-2 control as 3 frames at 11,025 Hz (data/php/mp3/falahati-php-mp3-control-audit.md). No lead remains unresolved (data/php/mp3/lead-audit.md). debach/zend-mp3 1.8.1 walks MPEG frames itself in Zend_Media_Mpeg_Abs, but its parent class file does not compile on PHP 8 (removed $str{$i} offsets), so it returns nothing on PHP 8.5. fobilow/mp3file has no release tag or license and also fails to compile. The re-scan found a native MPEG-1 Layer III decoder in xiaosongshu/flv2mp4 v1.8.7: 12,672 samples at 44.1 kHz on the MPEG-1 control, no frames on the MPEG-2 control, and its documented API decodes in a child process. holine/mp3 copies PHP-MP3 and does not return on either control. wapmorgan/media-file, dgoriaev/mp3info and acekyd/laravelmp3 delegate to or copy Mp3Info or getID3; phpvideotoolkit, mediaprobe, mp3php and soundfile hand parsing to FFmpeg or libsndfile. Two untagged CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, or MPEG-2.5 support.

[Ranking and search limits](../../../data/php/mp3/ranking.md) · [Standard API inventory](../../../data/php/mp3/standard.json)

## Third-party parsers

- [james-heinrich/getid3](james-heinrich-getid3/README.md) — verified Docker harness
- [wapmorgan/mp3info](wapmorgan-mp3info/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
