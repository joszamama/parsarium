# Go × WAV: verified parser ranking

21 verified third-party packages; working goal 20, original ceiling 30. The metric is pkg.go.dev's package-level ‘Imported by’ count captured at 2026-11-11T18:44:43.385680+00:00. It measures visible direct importers rather than downloads, and is used only within Go.

Search hits and unresolved leads are separate from this ranking. See `cell.json`, `registry-snapshot.json`, and `verification.json` in this directory.

| Rank | Package | Pinned module release | Imported by packages | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [github.com/go-audio/wav](https://pkg.go.dev/github.com/go-audio/wav@v1.1.0) | github.com/go-audio/wav@v1.1.0 | 314 | signs | mattetti/go-audio WAV lineage |
| 2 | [github.com/faiface/beep/wav](https://pkg.go.dev/github.com/faiface/beep/wav@v1.1.0) | github.com/faiface/beep@v1.1.0 | 223 | signs | beep WAV lineage |
| 3 | [github.com/hajimehoshi/ebiten/v2/audio/wav](https://pkg.go.dev/github.com/hajimehoshi/ebiten/v2/audio/wav@v2.10.6) | github.com/hajimehoshi/ebiten/v2@v2.10.6 | 163 | decoded_stereo_bytes | Ebitengine WAV decoder |
| 4 | [github.com/cryptix/wav](https://pkg.go.dev/github.com/cryptix/wav@v0.0.0-20180415113528-8bdace674401) | github.com/cryptix/wav@v0.0.0-20180415113528-8bdace674401 | 131 | sample_count | cryptix WAV reader |
| 5 | [github.com/youpy/go-wav](https://pkg.go.dev/github.com/youpy/go-wav@v0.3.2) | github.com/youpy/go-wav@v0.3.2 | 128 | signs | youpy WAV reader |
| 6 | [github.com/moutend/go-wav](https://pkg.go.dev/github.com/moutend/go-wav@v0.0.0-20170820031854-56127fbbb7ba) | github.com/moutend/go-wav@v0.0.0-20170820031854-56127fbbb7ba | 51 | signs | moutend WAV reader |
| 7 | [github.com/gopxl/beep/v2/wav](https://pkg.go.dev/github.com/gopxl/beep/v2/wav@v2.1.1) | github.com/gopxl/beep/v2@v2.1.1 | 27 | signs | beep WAV lineage |
| 8 | [azul3d.org/engine/audio/wav](https://pkg.go.dev/azul3d.org/engine/audio/wav@v0.0.0-20211024043305-793ea6c2839d) | azul3d.org/engine@v0.0.0-20211024043305-793ea6c2839d | 12 | format | azul3d WAV decoder |
| 9 | [github.com/mattetti/audio/wav](https://pkg.go.dev/github.com/mattetti/audio/wav@v0.0.0-20240411020228-c5379f9b5b61) | github.com/mattetti/audio@v0.0.0-20240411020228-c5379f9b5b61 | 9 | signs | mattetti/go-audio WAV lineage |
| 10 | [github.com/200sc/klangsynthese/wav](https://pkg.go.dev/github.com/200sc/klangsynthese/wav@v0.2.1) | github.com/200sc/klangsynthese@v0.2.1 | 9 | data_bytes | klangsynthese WAV reader |
| 11 | [github.com/unixpickle/wav](https://pkg.go.dev/github.com/unixpickle/wav@v0.0.0-20190525173943-42cf4c455f64) | github.com/unixpickle/wav@v0.0.0-20190525173943-42cf4c455f64 | 9 | signs | unixpickle WAV reader |
| 12 | [github.com/iFaceless/godub/wav](https://pkg.go.dev/github.com/iFaceless/godub/wav@v0.0.0-20200728093528-a30bb4d1a0f1) | github.com/iFaceless/godub@v0.0.0-20200728093528-a30bb4d1a0f1 | 8 | data_bytes | godub WAV reader |
| 13 | [github.com/cwbudde/wav](https://pkg.go.dev/github.com/cwbudde/wav@v0.1.4) | github.com/cwbudde/wav@v0.1.4 | 4 | sample_count | mattetti/go-audio WAV lineage |
| 14 | [github.com/qiniu/audio/wav](https://pkg.go.dev/github.com/qiniu/audio/wav@v0.2.1) | github.com/qiniu/audio@v0.2.1 | 4 | decoded_bytes | qiniu WAV reader |
| 15 | [github.com/inkyblackness/res/audio/wav](https://pkg.go.dev/github.com/inkyblackness/res/audio/wav@v0.0.0-20180728072643-e78e2ff1969d) | github.com/inkyblackness/res@v0.0.0-20180728072643-e78e2ff1969d | 4 | sample_count | inkyblackness WAV decoder |
| 16 | [github.com/xigh/go-wavreader](https://pkg.go.dev/github.com/xigh/go-wavreader@v0.0.0-20210516212152-f49019aa7352) | github.com/xigh/go-wavreader@v0.0.0-20210516212152-f49019aa7352 | 3 | frames | xigh WAV reader |
| 17 | [github.com/tphakala/go-wav/pcm](https://pkg.go.dev/github.com/tphakala/go-wav/pcm@v1.1.1) | github.com/tphakala/go-wav@v1.1.1 | 3 | data_bytes | tphakala WAV reader |
| 18 | [github.com/gonutz/mixer/wav](https://pkg.go.dev/github.com/gonutz/mixer/wav@v1.0.0) | github.com/gonutz/mixer@v1.0.0 | 1 | data_bytes | gonutz WAV reader |
| 19 | [github.com/yut-kt/gowave](https://pkg.go.dev/github.com/yut-kt/gowave@v0.1.4) | github.com/yut-kt/gowave@v0.1.4 | 1 | header | gowave reader |
| 20 | [github.com/weakpixel/voice/wav](https://pkg.go.dev/github.com/weakpixel/voice/wav@v0.0.1) | github.com/weakpixel/voice@v0.0.1 | 0 | signs | weakpixel WAV reader |
| 21 | [github.com/ngyewch/go-pcm/wav](https://pkg.go.dev/github.com/ngyewch/go-pcm/wav@v0.3.0) | github.com/ngyewch/go-pcm@v0.3.0 | 0 | data_bytes | go-pcm WAV reader |
