# MP3 / JavaScript — pilot

**Status:** pilot_five_selected_search_bounded; incomplete. 5 verified third-party paths, 0 verified standard APIs, 5 verified Docker harnesses.

Five verified paths; no padding. Search is six npm queries of 100 hits each, captured 2026-11-17; downloads were fetched for 15 hand-picked candidates, not every hit. mediabunny was found by `mp3 frame`, `mp3 duration` and `mp3 demuxer`, not the narrower queries. Download counts cover whole toolkits: mediabunny's muxing, conversion and many containers, and codec-parser's AAC, FLAC and Ogg parsers, not MP3 framing alone. The first three remain the highest-download fetched candidates; mp3-duration and mp3-parser have lower adoption. mp3-parser has 40,519 monthly downloads, below the duration-only leads, and is selected for its documented frame reader and exact whole-control walk. Its AFL++ differential is narrow: two source ranges in lib.js octetToBinRep bit extraction, not distinct version/channel branches. None decodes Layer III audio. The mpg123 WASM wrappers are recorded as shared-family leads. Two untagged CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, MPEG-2.5, CRC-protected or ID3 support. No standard Node.js MP3 API exists. codec-parser's valid-control AFL++ differential is narrow: one header-cache range that tracks distinct frame headers, not version or channel branches. Its V8 line counts include module evaluation of imported AAC, FLAC, Opus, Vorbis and Ogg files that audio/mpeg parsing does not call. music-metadata reports MPEG version and layer only through its codec string ('MPEG 1 Layer 3'), not as separate fields, and needs duration: true for a full frame walk. Its valid-control AFL++ differential is 4 sync() tail-policy ranges that track frame length, not version or channel branches. Its V8 package line count (3,539) is mostly module evaluation; MpegParser.js alone is 245 lines. mp3-duration exposes only duration; its count-scoped AFL signal tracks 11 versus 12 frame calls and may reflect input length, not a new branch or line. The same release is also verified for tagged MP3 duration in the ID3v2 cell.

[Ranking and search limits](../../../data/javascript/mp3/ranking.md) · [Standard API inventory](../../../data/javascript/mp3/standard.json)

## Third-party parsers

- [mediabunny](mediabunny/README.md) — verified Docker harness
- [music-metadata](music-metadata/README.md) — verified Docker harness
- [codec-parser](codec-parser/README.md) — verified Docker harness
- [mp3-duration](mp3-duration/README.md) — verified Docker harness
- [mp3-parser](mp3-parser/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
