# Go × MP3 with ID3v2: verified parser ranking

20 verified third-party packages; working goal 20, original ceiling 30. The metric is pkg.go.dev's package-level ‘Imported by’ count captured at 2026-11-11T19:19:51.493289+00:00. It measures visible direct importers rather than downloads, and is used only within Go.

Search hits and unresolved leads are separate from this ranking. See `cell.json`, `registry-snapshot.json`, and `verification.json` in this directory.

| Rank | Package | Pinned module release | Imported by packages | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [github.com/faiface/beep/mp3](https://pkg.go.dev/github.com/faiface/beep/mp3@v1.1.0) | github.com/faiface/beep@v1.1.0 | 444 | decoded samples and sample rate | hajime/go-mp3 via beep |
| 2 | [github.com/dhowden/tag](https://pkg.go.dev/github.com/dhowden/tag@v0.0.0-20240417053706-3d75831295e8) | github.com/dhowden/tag@v0.0.0-20240417053706-3d75831295e8 | 381 | ID3v2.3 title | dhowden/tag lineage |
| 3 | [github.com/hajimehoshi/go-mp3](https://pkg.go.dev/github.com/hajimehoshi/go-mp3@v0.3.4) | github.com/hajimehoshi/go-mp3@v0.3.4 | 294 | decoded PCM bytes and sample rate | hajime/go-mp3 lineage |
| 4 | [github.com/hajimehoshi/ebiten/v2/audio/mp3](https://pkg.go.dev/github.com/hajimehoshi/ebiten/v2/audio/mp3@v2.10.6) | github.com/hajimehoshi/ebiten/v2@v2.10.6 | 144 | decoded PCM bytes and sample rate | hajime/go-mp3 lineage |
| 5 | [github.com/bogem/id3v2/v2](https://pkg.go.dev/github.com/bogem/id3v2/v2@v2.1.4) | github.com/bogem/id3v2/v2@v2.1.4 | 72 | ID3v2.3 title | bogem ID3v2 parser |
| 6 | [github.com/tcolgate/mp3](https://pkg.go.dev/github.com/tcolgate/mp3@v0.0.0-20170426193717-e79c5a46d300) | github.com/tcolgate/mp3@v0.0.0-20170426193717-e79c5a46d300 | 62 | MPEG frame size and samples | tcolgate MP3 frame lineage |
| 7 | [github.com/gopxl/beep/v2/mp3](https://pkg.go.dev/github.com/gopxl/beep/v2/mp3@v2.1.1) | github.com/gopxl/beep/v2@v2.1.1 | 44 | decoded samples and sample rate | hajime/go-mp3 via beep |
| 8 | [github.com/tosone/minimp3](https://pkg.go.dev/github.com/tosone/minimp3@v1.1.0) | github.com/tosone/minimp3@v1.1.0 | 34 | decoded PCM bytes and audio format | minimp3 decoder |
| 9 | [github.com/ascherkus/go-id3/src/id3](https://pkg.go.dev/github.com/ascherkus/go-id3/src/id3@v0.0.0-20120522061058-b139b6a612de) | github.com/ascherkus/go-id3@v0.0.0-20120522061058-b139b6a612de | 6 | ID3v2.3 title | ascherkus/go-id3 lineage |
| 10 | [github.com/dustin/go-id3](https://pkg.go.dev/github.com/dustin/go-id3@v0.0.0-20131108194644-73f4b1cf2a4e) | github.com/dustin/go-id3@v0.0.0-20131108194644-73f4b1cf2a4e | 5 | ID3v2.3 title | ascherkus/go-id3 lineage |
| 11 | [github.com/icanhazbroccoli/tag](https://pkg.go.dev/github.com/icanhazbroccoli/tag@v0.0.0-20210306220707-0c387c570328) | github.com/icanhazbroccoli/tag@v0.0.0-20210306220707-0c387c570328 | 4 | ID3v2.3 title | dhowden/tag lineage |
| 12 | [honnef.co/go/id3](https://pkg.go.dev/honnef.co/go/id3@v0.0.0-20250113165337-e36fa5d059c5) | honnef.co/go/id3@v0.0.0-20250113165337-e36fa5d059c5 | 3 | ID3v2.3 title | honnef ID3 parser |
| 13 | [github.com/dece2183/go-stream-mp3](https://pkg.go.dev/github.com/dece2183/go-stream-mp3@v1.0.2) | github.com/dece2183/go-stream-mp3@v1.0.2 | 2 | decoded PCM bytes and sample rate | hajime/go-mp3 lineage |
| 14 | [github.com/fgergo/mp3](https://pkg.go.dev/github.com/fgergo/mp3@v1.0.0) | github.com/fgergo/mp3@v1.0.0 | 2 | MPEG frame size and samples | tcolgate MP3 frame lineage |
| 15 | [github.com/mattetti/audio/mp3](https://pkg.go.dev/github.com/mattetti/audio/mp3@v0.0.0-20240411020228-c5379f9b5b61) | github.com/mattetti/audio@v0.0.0-20240411020228-c5379f9b5b61 | 2 | reported duration and frame count | tcolgate MP3 frame lineage |
| 16 | [github.com/qiniu/audio/mp3](https://pkg.go.dev/github.com/qiniu/audio/mp3@v0.2.1) | github.com/qiniu/audio@v0.2.1 | 2 | decoded PCM bytes and audio format | hajime/go-mp3 wrapper |
| 17 | [github.com/sa6mwa/mp3duration](https://pkg.go.dev/github.com/sa6mwa/mp3duration@v0.0.0-20221104103912-0716b1a5de6e) | github.com/sa6mwa/mp3duration@v0.0.0-20221104103912-0716b1a5de6e | 2 | reported duration and frame count | sa6mwa MP3 duration reader |
| 18 | [github.com/gcottom/mp3meta](https://pkg.go.dev/github.com/gcottom/mp3meta@v0.0.4) | github.com/gcottom/mp3meta@v0.0.4 | 2 | ID3v2.3 title | gcottom MP3 tag reader |
| 19 | [github.com/guregu/tag](https://pkg.go.dev/github.com/guregu/tag@v0.0.3) | github.com/guregu/tag@v0.0.3 | 2 | ID3v2.3 title | dhowden/tag lineage |
| 20 | [github.com/frolovo22/tag](https://pkg.go.dev/github.com/frolovo22/tag@v0.0.2) | github.com/frolovo22/tag@v0.0.2 | 2 | ID3v2.3 title with trailing NUL | frolovo22 ID3 parser |
