# mp3-duration — MP3 / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.1.0`
- **License:** MIT
- **Parser family:** mp3-duration JavaScript MPEG frame-header scanner
- **Local input API:** `mp3Duration(Buffer, false) Promise on local file bytes; false disables the CBR size estimate so index.js scans frame headers to EOF`
- **Documentation:** [API reference](<https://github.com/ddsol/mp3-duration/blob/20bda6406e92ad200f5774d3a88ae2d9dc1e2cbc/README.md>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3/parsers.json) · [control result](../../../../projects/mp3/javascript/mp3_duration/verification.json)

## Observed control result

```json
{
  "duration_ms": 287
}
```

## Verification scope

Both untagged valid controls return 287 and 313 duration_ms, matching the independent frame-header walker (11 MPEG-1 frames of 1152 samples/44100 Hz and 12 MPEG-2 frames of 576 samples/22050 Hz, rounded to milliseconds). The package scans headers through index.js with cbrEstimate=false rather than estimating from file length; it exposes no frame metadata or audio decode. Docker V8 covers 156 own index.js lines. Opt-in AFL++ feedback uses only parseFrameHeader and frameSize range hit counts, capped at 255, giving 11 versus 12 calls with three stable repeats and zero parser features on module-load-only baseline. This tracks frame count and possibly input length; it is not new line or branch coverage. The same release is separately verified in mp3_id3v2/javascript for duration scope. Two short CBR controls do not establish VBR, free-format or other MPEG layer support; no malformed/resource-use/campaign tests were run.

## Run this target

```sh
python3 parsarium.py build mp3 javascript mp3_duration
python3 parsarium.py run mp3 javascript mp3_duration controls/mp3/tone-44k-mono.mp3
```
