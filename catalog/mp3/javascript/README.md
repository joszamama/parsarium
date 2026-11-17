# MP3 / JavaScript — pilot

**Status:** pilot_one_selected_search_bounded; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

One verified path; no padding. Search is six npm queries of 100 hits each, captured 2026-11-17; downloads were fetched for 15 hand-picked candidates, not every hit. mediabunny was found by `mp3 frame`, `mp3 duration` and `mp3 demuxer`, not the narrower queries. Its download count covers the whole media toolkit (muxing, conversion, many containers), not MP3 demuxing alone. The path demuxes frames and reads headers but does not decode Layer III audio (that would need WebCodecs). mediabunny is not among the mp3_id3v2/javascript paths; music-metadata and the mpg123 WASM wrappers are recorded as shared-family leads. Two untagged CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, or MPEG-2.5 support. No standard Node.js MP3 API exists.

[Ranking and search limits](../../../data/javascript/mp3/ranking.md) · [Standard API inventory](../../../data/javascript/mp3/standard.json)

## Third-party parsers

- [mediabunny](mediabunny/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
