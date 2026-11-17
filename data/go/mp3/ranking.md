# Go plain MP3 parser pilot

Seven third-party paths are verified against valid untagged MPEG Layer III controls. The ceiling is ten; the remaining recorded leads are unresolved, excluded, or share selected parser families.

## Within-cell adoption metric

pkg.go.dev **Imported by** package count from the [saved search snapshot](registry-snapshot.json). It measures package adoption, not MP3-specific use or independent parser families.

| Rank | Package | Release | Imported by | Observed parsing scope |
| ---: | --- | --- | ---: | --- |
| 1 | [faiface/beep/mp3](../../../projects/mp3/go/github_com_faiface_beep_mp3/README.md) | v1.1.0 | 444 | `Decode(io.ReadCloser)` streams float64 samples; wrapper over go-mp3 v0.3.0 |
| 2 | [hajimehoshi/go-mp3](../../../projects/mp3/go/github_com_hajimehoshi_go_mp3/README.md) | v0.3.4 | 294 | `NewDecoder(io.Reader)` decodes untagged MPEG Layer III frames to PCM |
| 3 | [hajimehoshi/ebiten/v2/audio/mp3](../../../projects/mp3/go/github_com_hajimehoshi_ebiten_v2_audio_mp3/README.md) | v2.10.6 | 144 | `DecodeWithoutResampling(io.Reader)` returns 16-bit PCM; wrapper over go-mp3 v0.3.4 |
| 4 | [tcolgate/mp3](../../../projects/mp3/go/github_com_tcolgate_mp3/README.md) | v0.0.0-20170426193717-e79c5a46d300 | 62 | `NewDecoder(io.Reader)` parses full frame headers and side information; no PCM decoder |
| 5 | [gopxl/beep/v2/mp3](../../../projects/mp3/go/github_com_gopxl_beep_v2_mp3/README.md) | v2.1.1 | 44 | `Decode(io.ReadCloser)` streams float64 samples; wrapper over go-mp3 v0.3.4 |
| 6 | [tosone/minimp3](../../../projects/mp3/go/github_com_tosone_minimp3/README.md) | v1.1.0 | 34 | `DecodeFull([]byte)` invokes the vendored native C Layer III decoder through cgo and returns PCM |
| 7 | [dmulholl/mp3lib](../../../projects/mp3/go/github_com_dmulholl_mp3lib/README.md) | v1.0.0 | 9 | `NextFrame(io.Reader)` parses full frame headers and boundaries; no PCM decoder |

Four parser families are represented. hajimehoshi/go-mp3, tcolgate/mp3, dmulholl/mp3lib and tosone/minimp3 (native minimp3) each carry their own decoder or frame parser. faiface/beep/mp3, hajimehoshi/ebiten/v2/audio/mp3 and gopxl/beep/v2/mp3 are counted as separate package APIs with their own metrics, but delegate decoding to go-mp3. Their Docker coverage counts wrapper lines and go-mp3 lines separately, and every AFL++ tuple difference between the two controls lies in go-mp3. faiface/beep v1.1.0 resolves the older go-mp3 v0.3.0; the other wrappers use the selected v0.3.4. The ranking is by package adoption and does not count independent decoders.

The go-mp3 and tcolgate/mp3 package paths are also represented in the tagged MP3 cell, so their parser-family lineage is recorded across cells. The two plain-MP3 controls are 11 MPEG-1 mono 44.1 kHz frames and 12 MPEG-2 stereo 22.05 kHz frames. All seven paths have Docker harnesses, source coverage, and repeat-stable AFL++ feedback with a valid-control differential. For tosone/minimp3, source coverage distinguishes its Go binding from the native `minimp3.h` decoder; AFL++ instruments only allowlisted native decoder functions. PCM and sample hashes are toolchain-specific and are not compared across decoders or releases.

The five pkg.go.dev queries were bounded at 100 hits each: 313 hits and 242 distinct package paths. [Leads](leads.json) records 39 inspected candidates: 6 selected, 3 shared-family, 25 excluded, 5 unresolved. derat/mpeg ([probe](probes/derat_mpeg/README.md)) and mattetti/audio/mp3 ([probe](probes/mattetti_audio_mp3/README.md)) parse both valid controls, but each covers the same parser blocks on both, so they fail the feedback gate. fgergo/mp3 is a byte-identical fork of tcolgate/mp3 ([comparison](probes/fgergo_mp3/README.md)). The remaining go-mp3, tcolgate and minimp3 wrappers and the cgo libmpg123 wrapper are unresolved and not harnessed. The selection is not a definitive top-ten ranking. Two constant-bitrate controls do not establish VBR, Xing/Info, free-format, other MPEG layers, or ID3 handling.
