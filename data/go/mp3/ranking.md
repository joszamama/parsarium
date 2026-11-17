# Go plain MP3 parser pilot

Two third-party paths are verified against valid untagged MPEG Layer III controls. The ceiling is ten; the remaining recorded leads are unresolved or share selected parser families.

## Within-cell adoption metric

pkg.go.dev **Imported by** package count from the [saved search snapshot](registry-snapshot.json). It measures package adoption, not MP3-specific use or independent parser families.

| Rank | Package | Release | Imported by | Observed parsing scope |
| ---: | --- | --- | ---: | --- |
| 1 | [hajimehoshi/go-mp3](../../../projects/mp3/go/github_com_hajimehoshi_go_mp3/README.md) | v0.3.4 | 294 | `NewDecoder(io.Reader)` decodes untagged MPEG Layer III frames to PCM |
| 2 | [tcolgate/mp3](../../../projects/mp3/go/github_com_tcolgate_mp3/README.md) | v0.0.0-20170426193717-e79c5a46d300 | 62 | `NewDecoder(io.Reader)` parses full frame headers and side information; no PCM decoder |

Both package paths are also represented in the tagged MP3 cell, so their parser-family lineage is recorded across cells. The two plain-MP3 controls are 11 MPEG-1 mono 44.1 kHz frames and 12 MPEG-2 stereo 22.05 kHz frames. Each path has a Docker harness, source coverage, and repeat-stable AFL++ feedback with a valid-control differential.

The five pkg.go.dev queries were bounded at 100 hits each: 313 hits and 242 distinct package paths. [Leads](leads.json) records 14 inspected candidates; six remain unresolved, three are known shared-family wrappers, and four are excluded. The selection is not a definitive top-ten ranking. Two constant-bitrate controls do not establish VBR, Xing/Info, free-format, other MPEG layers, or ID3 handling.
