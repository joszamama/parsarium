# MP3 / Python — pilot

**Status:** pilot_two_verified_bounded_search; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Two verified paths; no padding. The name search is a substring filter over the PyPI Simple index (serial 43764887) captured 2026-11-17; the 'mp3' and 'mpeg' hit lists were not triaged one by one, and download numbers were fetched only for 13 named candidates, so a less obvious frame parser could be missed. Native wrappers (av, soundfile, audioread, pygame, pymediainfo, miniaudio) are unresolved, not rejected: their parsers are real but outside Python source coverage. eyed3, hachoir and pymp3 are unresolved pure-Python leads. Mutagen reads headers and checks frame syncs but does not decode audio; for CBR streams without Xing/Info/VBRI its duration is stream bytes divided by the first header's bitrate. TinyTag also only reads headers: after five equal-bitrate frames it estimates duration from stream size and mean frame length, and it does not expose MPEG version, layer or frame count. Both full-length controls run the same TinyTag lines; its feedback difference is shown with a valid three-frame prefix of the 44.1 kHz control. Two untagged CBR controls do not establish VBR, free-format, Layer I/II, or MPEG-2.5 support.

[Ranking and search limits](../../../data/python/mp3/ranking.md) · [Standard API inventory](../../../data/python/mp3/standard.json)

## Third-party parsers

- [mutagen](mutagen/README.md) — verified Docker harness
- [tinytag](tinytag/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
