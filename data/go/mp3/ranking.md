# Go plain MP3 parser pilot

Four third-party paths are verified against valid untagged MPEG Layer III controls. The ceiling is ten; the remaining recorded leads are unresolved or share selected parser families.

## Within-cell adoption metric

pkg.go.dev **Imported by** package count from the [saved search snapshot](registry-snapshot.json). It measures package adoption, not MP3-specific use or independent parser families.

| Rank | Package | Release | Imported by | Observed parsing scope |
| ---: | --- | --- | ---: | --- |
| 1 | [hajimehoshi/go-mp3](../../../projects/mp3/go/github_com_hajimehoshi_go_mp3/README.md) | v0.3.4 | 294 | `NewDecoder(io.Reader)` decodes untagged MPEG Layer III frames to PCM |
| 2 | [tcolgate/mp3](../../../projects/mp3/go/github_com_tcolgate_mp3/README.md) | v0.0.0-20170426193717-e79c5a46d300 | 62 | `NewDecoder(io.Reader)` parses full frame headers and side information; no PCM decoder |
| 3 | [tosone/minimp3](../../../projects/mp3/go/github_com_tosone_minimp3/README.md) | v1.1.0 | 34 | `DecodeFull([]byte)` invokes the vendored native C Layer III decoder through cgo and returns PCM |
| 4 | [dmulholl/mp3lib](../../../projects/mp3/go/github_com_dmulholl_mp3lib/README.md) | v1.0.0 | 9 | `NextFrame(io.Reader)` parses full frame headers and boundaries; no PCM decoder |

The first two package paths are also represented in the tagged MP3 cell, so their parser-family lineage is recorded across cells. The two plain-MP3 controls are 11 MPEG-1 mono 44.1 kHz frames and 12 MPEG-2 stereo 22.05 kHz frames. All four paths have Docker harnesses, source coverage, and repeat-stable AFL++ feedback with a valid-control differential. For tosone/minimp3, source coverage distinguishes its Go binding from the native `minimp3.h` decoder; AFL++ instruments only allowlisted native decoder functions. Its pinned PCM hashes are toolchain-specific and are not compared with another decoder's PCM.

The five pkg.go.dev queries were bounded at 100 hits each: 313 hits and 242 distinct package paths. [Leads](leads.json) records 14 inspected candidates; three remain unresolved, four are known shared-family wrappers or forks, and four are excluded. The selection is not a definitive top-ten ranking. Two constant-bitrate controls do not establish VBR, Xing/Info, free-format, other MPEG layers, or ID3 handling.
