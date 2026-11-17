# MP3 / Go — pilot

**Status:** pilot_seven_verified_bounded_search; incomplete. 7 verified third-party paths, 0 verified standard APIs, 7 verified Docker harnesses.

Seven verified Go plain-MP3 paths; korandiz/mpa v1.0.0 is excluded by a pinned valid MPEG-2 control that yields zero frames and unexpected EOF, matching its MPEG-1-only header check; no padding. Five pkg.go.dev queries were bounded at 100 hits each (313 hits, 242 unique). Every hit with at least two Imported by packages is now a selected path or a recorded lead. Of the 13 one-importer hits, only sdobz/go-mpg123, a distinct decoder family, is recorded; the others were judged from path and synopsis only (go-mp3 or tcolgate forks by name, tag readers, a video converter, and HLS or livego copies). 39 leads are recorded: five remain unresolved (go-mp3 wrappers pipelined.dev/audio/mp3 and qiniu/audio/mp3, tcolgate wrapper sa6mwa/mp3duration, cgo minimp3 binding cowork-ai/go-minimp3 and cgo libmpg123 wrapper sdobz/go-mpg123, none harnessed), and three are unselected shared-family forks or wrappers. derat/mpeg and mattetti/audio/mp3 parse both valid controls correctly but are excluded by the feedback gate, because each control pair covers identical parser blocks. fgergo/mp3 is a byte-identical fork of tcolgate/mp3 (15 of 16 files identical) and is not counted. pkg.go.dev Imported by counts package adoption rather than MP3-specific use, and wrapper counts are not independent decoder adoption. The hajimehoshi/go-mp3 and tcolgate/mp3 families are also represented in the tagged MP3 cell; the plain-frame routes are separate format paths, not new cross-cell families. Two untagged constant-bitrate controls do not establish VBR, Xing/Info, free-format, other MPEG layers, or ID3 handling. minimp3 PCM hashes are pinned to the Clang-built linux/arm64 image, and Beep float64 sample hashes to their go-mp3 release on linux/arm64; neither is compared across toolchains or releases.

[Ranking and search limits](../../../data/go/mp3/ranking.md) · [Standard API inventory](../../../data/go/mp3/standard.json)

## Third-party parsers

- [github.com/faiface/beep/mp3](github-com-faiface-beep-mp3/README.md) — verified Docker harness
- [github.com/hajimehoshi/go-mp3](github-com-hajimehoshi-go-mp3/README.md) — verified Docker harness
- [github.com/hajimehoshi/ebiten/v2/audio/mp3](github-com-hajimehoshi-ebiten-v2-audio-mp3/README.md) — verified Docker harness
- [github.com/tcolgate/mp3](github-com-tcolgate-mp3/README.md) — verified Docker harness
- [github.com/gopxl/beep/v2/mp3](github-com-gopxl-beep-v2-mp3/README.md) — verified Docker harness
- [github.com/tosone/minimp3](github-com-tosone-minimp3/README.md) — verified Docker harness
- [github.com/dmulholl/mp3lib](github-com-dmulholl-mp3lib/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
