# MP3 / Java — pilot

**Status:** pilot_four_selected_search_bounded; incomplete. 4 verified third-party paths, 0 verified standard APIs, 4 verified Docker harnesses.

Four pure-Java Layer III paths verified; no padding. jaudiotagger is header-only and its higher-level MP3AudioHeader(File) misidentifies the valid 22.05 kHz control start at byte 104 and estimates 5 rather than 12 frames; the selected first-header API reports only independently correct fields. Maven Central phrase queries returned no hits, so named leads were inspected via deps.dev and package documentation. deps.dev counts whole-package dependency use, not MP3-specific calls. Two untagged CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, MPEG-2.5 or ID3 behavior. Java SE 25 exports no MP3 reader by inventory.

[Ranking and search limits](../../../data/java/mp3/ranking.md) · [Standard API inventory](../../../data/java/mp3/standard.json)

## Third-party parsers

- [jcodec](jcodec/README.md) — verified Docker harness
- [mp3spi](mp3spi/README.md) — verified Docker harness
- [jlayer](jlayer/README.md) — verified Docker harness
- [jaudiotagger](jaudiotagger/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
