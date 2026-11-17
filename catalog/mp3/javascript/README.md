# MP3 / JavaScript — pilot

**Status:** pilot_four_selected_search_bounded; incomplete. 4 verified third-party paths, 0 verified standard APIs, 4 verified Docker harnesses.

Four frame-aware JavaScript paths are verified on the two valid untagged MP3 controls. mediabunny, music-metadata and codec-parser are the highest-download fetched candidates; mp3-parser is a lower-adoption, format-specific frame reader with an exact whole-file walk. Each path has package source coverage and parser-derived AFL++ feedback. None decodes Layer III audio. Search limits, family notes and control boundaries are in the ranking. The Node.js standard API inventory found no MP3 parser.

[Ranking and search limits](../../../data/javascript/mp3/ranking.md) · [Standard API inventory](../../../data/javascript/mp3/standard.json)

## Third-party parsers

- [mediabunny](mediabunny/README.md) — verified Docker harness
- [music-metadata](music-metadata/README.md) — verified Docker harness
- [codec-parser](codec-parser/README.md) — verified Docker harness
- [mp3-parser](mp3-parser/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
