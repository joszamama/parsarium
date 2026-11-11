# Go × MP4: verified parser ranking

20 verified third-party packages; working goal 20, original ceiling 30. The metric is pkg.go.dev's package-level ‘Imported by’ count captured at 2026-11-11T19:11:56.019162+00:00. It measures visible direct importers rather than downloads, and is used only within Go.

Search hits and unresolved leads are separate from this ranking. See `cell.json`, `registry-snapshot.json`, and `verification.json` in this directory.

| Rank | Package | Pinned module release | Imported by packages | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [github.com/dhowden/tag](https://pkg.go.dev/github.com/dhowden/tag@v0.0.0-20240417053706-3d75831295e8) | github.com/dhowden/tag@v0.0.0-20240417053706-3d75831295e8 | 381 | MP4 title | dhowden/tag lineage |
| 2 | [github.com/Eyevinn/mp4ff/mp4](https://pkg.go.dev/github.com/Eyevinn/mp4ff/mp4@v0.62.1) | github.com/Eyevinn/mp4ff@v0.62.1 | 103 | brand and track count | mp4ff lineage |
| 3 | [github.com/abema/go-mp4](https://pkg.go.dev/github.com/abema/go-mp4@v1.7.4) | github.com/abema/go-mp4@v1.7.4 | 72 | movie box | go-mp4 box parser |
| 4 | [github.com/nareix/joy4/format/mp4](https://pkg.go.dev/github.com/nareix/joy4/format/mp4@v0.0.0-20200507095837-05a4ffbb5369) | github.com/nareix/joy4@v0.0.0-20200507095837-05a4ffbb5369 | 40 | stream count | joy4 MP4 lineage |
| 5 | [github.com/yapingcat/gomedia/go-mp4](https://pkg.go.dev/github.com/yapingcat/gomedia/go-mp4@v0.0.0-20240906162731-17feea57090c) | github.com/yapingcat/gomedia@v0.0.0-20240906162731-17feea57090c | 23 | track count | gomedia MP4 lineage |
| 6 | [github.com/deepch/vdk/format/mp4](https://pkg.go.dev/github.com/deepch/vdk/format/mp4@v0.0.27) | github.com/deepch/vdk@v0.0.27 | 22 | stream count | joy4 MP4 lineage |
| 7 | [github.com/alfg/mp4](https://pkg.go.dev/github.com/alfg/mp4@v0.0.0-20210728035756-55ea58c08aeb) | github.com/alfg/mp4@v0.0.0-20210728035756-55ea58c08aeb | 17 | major brand | alfg MP4 reader |
| 8 | [github.com/jfbus/mp4](https://pkg.go.dev/github.com/jfbus/mp4@v0.0.0-20150401112544-b5bc0819ce33) | github.com/jfbus/mp4@v0.0.0-20150401112544-b5bc0819ce33 | 13 | ftyp brand only | jfbus MP4 lineage |
| 9 | [github.com/MStoykov/mp4](https://pkg.go.dev/github.com/MStoykov/mp4@v0.1.4) | github.com/MStoykov/mp4@v0.1.4 | 10 | major brand | jfbus MP4 lineage |
| 10 | [go4.org/media/heif/bmff](https://pkg.go.dev/go4.org/media/heif/bmff@v0.0.0-20261028031214-ed6929a230fe) | go4.org@v0.0.0-20261028031214-ed6929a230fe | 9 | ftyp brand only | go4 ISO BMFF reader |
| 11 | [github.com/Sorrow446/go-mp4tag](https://pkg.go.dev/github.com/Sorrow446/go-mp4tag@v0.0.0-20240130220823-68ce31d53e37) | github.com/Sorrow446/go-mp4tag@v0.0.0-20240130220823-68ce31d53e37 | 5 | MP4 title | Sorrow446 MP4 tag reader |
| 12 | [github.com/gcottom/mp4meta](https://pkg.go.dev/github.com/gcottom/mp4meta@v0.0.5) | github.com/gcottom/mp4meta@v0.0.5 | 3 | MP4 title | gcottom MP4 tag reader |
| 13 | [github.com/guregu/tag](https://pkg.go.dev/github.com/guregu/tag@v0.0.3) | github.com/guregu/tag@v0.0.3 | 2 | MP4 title | dhowden/tag lineage |
| 14 | [github.com/frolovo22/tag](https://pkg.go.dev/github.com/frolovo22/tag@v0.0.2) | github.com/frolovo22/tag@v0.0.2 | 2 | MP4 title | frolovo22 MP4 tag reader |
| 15 | [github.com/rcarmo/go-264/audio/mp4](https://pkg.go.dev/github.com/rcarmo/go-264/audio/mp4@v0.0.0-20261008100743-cecca3835cbd) | github.com/rcarmo/go-264@v0.0.0-20261008100743-cecca3835cbd | 1 | track count | go-264 MP4 audio demuxer |
| 16 | [github.com/edgeware/mp4ff/mp4](https://pkg.go.dev/github.com/edgeware/mp4ff/mp4@v0.31.0) | github.com/edgeware/mp4ff@v0.31.0 | 0 | brand and track count | mp4ff lineage |
| 17 | [github.com/eluv-io/mp4ff/mp4](https://pkg.go.dev/github.com/eluv-io/mp4ff/mp4@v0.48.0) | github.com/eluv-io/mp4ff@v0.48.0 | 0 | brand and track count | mp4ff lineage |
| 18 | [github.com/montybay/mp4ff/mp4](https://pkg.go.dev/github.com/montybay/mp4ff/mp4@v0.0.0-20261017003302-c9570d1e4b3c) | github.com/montybay/mp4ff@v0.0.0-20261017003302-c9570d1e4b3c | 0 | brand and track count | mp4ff lineage |
| 19 | [github.com/tetsuo/mp4](https://pkg.go.dev/github.com/tetsuo/mp4@v0.3.0) | github.com/tetsuo/mp4@v0.3.0 | 0 | ftyp brand only | tetsuo MP4 box reader |
| 20 | [github.com/ntklink/gomediautils/go-mp4](https://pkg.go.dev/github.com/ntklink/gomediautils/go-mp4@v0.0.0-20260924103313-787406a6c4b3) | github.com/ntklink/gomediautils@v0.0.0-20260924103313-787406a6c4b3 | 0 | track count | gomedia MP4 lineage |
