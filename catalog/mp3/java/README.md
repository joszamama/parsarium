# MP3 / Java — pilot

**Status:** pilot_one_selected_search_bounded; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

Pilot cell: only the highest-adoption pure-Java Layer III path was built and control-verified; no padding. Maven Central Solr search ranks by relevance, the phrase queries 'mp3 decoder' and 'mpeg audio' returned 0 hits, so leads were looked up directly on deps.dev and logged in leads.json. deps.dev public coverage is incomplete and jcodec's count covers the whole codec library, not MP3 use alone. Two untagged CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, MPEG-2.5 or intensity-stereo support; jcodec's Mp3Decoder throws on intensity stereo by design. Java SE 25 exports no MP3 API, so the standard count is zero by inventory.

[Ranking and search limits](../../../data/java/mp3/ranking.md) · [Standard API inventory](../../../data/java/mp3/standard.json)

## Third-party parsers

- [jcodec](jcodec/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
