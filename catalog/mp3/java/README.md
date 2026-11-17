# MP3 / Java — pilot

**Status:** pilot_five_selected_search_bounded; incomplete. 5 verified third-party paths, 0 verified standard APIs, 5 verified Docker harnesses.

Five pure-Java Layer III paths verified; no padding. jaudiotagger is first-header-only and mp3agic reports only accurate header fields. Both higher-level APIs misidentify the valid 22.05 kHz control start at byte 104 and estimate 5 rather than 12 frames; mp3agic reports 261 ms versus oracle about 313 ms. These paths make no whole-file frame-count or duration claim. JavaMP3 1.0.1 decodes the mono control exactly but crashes on valid 22.05 kHz stereo input, so is excluded with a reproducible probe. Maven Central phrase queries returned no hits, so named leads were inspected via deps.dev and package documentation. deps.dev counts whole-package dependency use, not MP3-specific calls. Two untagged CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, MPEG-2.5 or ID3 behavior. Java SE 25 exports no MP3 reader by inventory.

[Ranking and search limits](../../../data/java/mp3/ranking.md) · [Standard API inventory](../../../data/java/mp3/standard.json)

## Third-party parsers

- [jcodec](jcodec/README.md) — verified Docker harness
- [mp3spi](mp3spi/README.md) — verified Docker harness
- [jlayer](jlayer/README.md) — verified Docker harness
- [jaudiotagger](jaudiotagger/README.md) — verified Docker harness
- [mp3agic](mp3agic/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
