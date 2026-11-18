# GO × MP3: selected parsers

10 control-verified third-party paths selected from 11 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

pkg.go.dev Imported by package count.

| Rank | Package | Release | Imported by (pkg.go.dev) | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [github.com/faiface/beep/mp3](https://pkg.go.dev/github.com/faiface/beep/mp3@v1.1.0) | v1.1.0 | 444 | decoded samples and sample rate | hajime/go-mp3 via beep |
| 2 | [github.com/dhowden/tag](https://pkg.go.dev/github.com/dhowden/tag@v0.0.0-20240417053706-3d75831295e8) | v0.0.0-20240417053706-3d75831295e8 | 381 | ID3v2.3 title | dhowden/tag lineage |
| 3 | [github.com/hajimehoshi/go-mp3](https://pkg.go.dev/github.com/hajimehoshi/go-mp3@v0.3.4) | v0.3.4 | 294 | decoded PCM bytes and sample rate | hajime/go-mp3 lineage |
| 4 | [github.com/hajimehoshi/ebiten/v2/audio/mp3](https://pkg.go.dev/github.com/hajimehoshi/ebiten/v2/audio/mp3@v2.10.6) | v2.10.6 | 144 | decoded PCM bytes and sample rate | hajime/go-mp3 lineage |
| 5 | [github.com/bogem/id3v2/v2](https://pkg.go.dev/github.com/bogem/id3v2/v2@v2.1.4) | v2.1.4 | 72 | ID3v2.3 title | bogem ID3v2 parser |
| 6 | [github.com/tcolgate/mp3](https://pkg.go.dev/github.com/tcolgate/mp3@v0.0.0-20170426193717-e79c5a46d300) | v0.0.0-20170426193717-e79c5a46d300 | 62 | MPEG frame size and samples | tcolgate MP3 frame lineage |
| 7 | [github.com/gopxl/beep/v2/mp3](https://pkg.go.dev/github.com/gopxl/beep/v2/mp3@v2.1.1) | v2.1.1 | 44 | decoded samples and sample rate | hajime/go-mp3 via beep |
| 8 | [github.com/tosone/minimp3](https://pkg.go.dev/github.com/tosone/minimp3@v1.1.0) | v1.1.0 | 34 | decoded PCM bytes and audio format | minimp3 decoder |
| 9 | [github.com/dmulholl/mp3lib](https://pkg.go.dev/github.com/dmulholl/mp3lib@v1.0.0) | v1.0.0 | 9 | MPEG Layer III frame headers and frame boundaries from untagged local bytes; no PCM decoding | dmulholl/mp3lib frame parser |
| 10 | [github.com/ascherkus/go-id3/src/id3](https://pkg.go.dev/github.com/ascherkus/go-id3/src/id3@v0.0.0-20120522061058-b139b6a612de) | v0.0.0-20120522061058-b139b6a612de | 6 | ID3v2.3 title | ascherkus/go-id3 lineage |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
