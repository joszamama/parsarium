# MP3 / C — pilot

**Status:** pilot_one_verified_bounded_search; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

One verified path; no padding. Search is a substring match over all Homebrew formula names and descriptions for seven queries, captured 2026-11-17; it misses header-only decoders that are not packaged there. minimp3 and dr_mp3 have no value on the primary metric, so their GitHub stars are recorded as supplemental only and are not compared with Homebrew counts. libmad is an unresolved independent family. Homebrew installs measure macOS/Linux package demand for the whole mpg123 distribution (player and library), not direct use of the decoding API. libmpg123 is the same engine counted under mp3_id3v2/c. Two untagged CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, or MPEG-2.5 support.

[Ranking and search limits](../../../data/c/mp3/ranking.md) · [Standard API inventory](../../../data/c/mp3/standard.json)

## Third-party parsers

- [mpg123](mpg123/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
