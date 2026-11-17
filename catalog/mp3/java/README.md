# MP3 / Java — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Pilot cell: two pure-Java MPEG Layer III paths verified; no padding. Maven Central Solr phrase queries returned no hits, so named leads were inspected via deps.dev and Maven documentation. deps.dev coverage is incomplete and counts all dependency use of each package, not MP3-specific calls. The higher-count mp3spi Java Sound SPI wrapper over soundlibs JLayer remains unverified. Two untagged CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, MPEG-2.5 or ID3 behavior. Java SE 25 exports no MP3 reader by inventory.

[Ranking and search limits](../../../data/java/mp3/ranking.md) · [Standard API inventory](../../../data/java/mp3/standard.json)

## Third-party parsers

- [jcodec](jcodec/README.md) — verified Docker harness
- [jlayer](jlayer/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
