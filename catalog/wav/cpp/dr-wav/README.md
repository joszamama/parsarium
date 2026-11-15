# dr_wav — WAV / C++

- **Pinned release:** `wav-0.14.6`
- **License:** MIT-0
- **Parsed scope:** WAV sample rate, channel and frame counts, plus first four decoded PCM samples
- **Underlying family:** dr_wav C WAV decoder
- **Local input API:** `drwav_init_file; drwav_read_pcm_frames_s16; totalPCMFrameCount`
- **Documentation:** [API reference](<https://github.com/mackron/dr_libs/blob/wav-0.14.6/dr_wav.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/wav/parsers.json) · [control verification](../../../../data/cpp/wav/verification.json) · [within-ecosystem ranking](../../../../data/cpp/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "frames": 4,
  "samples": [
    0,
    1000,
    -1000,
    0
  ]
}
```

Standalone dr_wav release in dr_libs; miniaudio embeds dr_wav lineage. The C++ path uses the exact C-cell release and underlying decoder.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/cpp/dr_wav/README.md)

```sh
python3 parsarium.py build wav cpp dr_wav
python3 parsarium.py run wav cpp dr_wav controls/wav/four-samples.wav
```
