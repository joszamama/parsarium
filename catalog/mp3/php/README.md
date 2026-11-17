# MP3 / PHP — pilot

**Status:** pilot_one_verified_bounded_search; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

One verified path; no padding. Search is seven Packagist search.json queries capped at 50 hits each, captured 2026-11-17; package descriptions alone decided most exclusions. Packagist total downloads count Composer installs of the whole package (and wrappers pull getID3 transitively), not use of the MPEG frame parser. getID3 reads the first frame header, checks sync on following frames, and derives CBR duration from audio-data bytes and the header bitrate; it does not decode audio or report a frame count on these controls. Mp3Info, PHP-MP3 (falahati/php-mp3), the Zend media reader and fobilow/mp3file are unresolved independent candidates. Two untagged CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, or MPEG-2.5 support.

[Ranking and search limits](../../../data/php/mp3/ranking.md) · [Standard API inventory](../../../data/php/mp3/standard.json)

## Third-party parsers

- [james-heinrich/getid3](james-heinrich-getid3/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
