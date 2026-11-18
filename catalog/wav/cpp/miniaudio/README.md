# miniaudio — WAV / C++

- **Pinned release:** `0.11.26`
- **Upstream:** [source repository](<https://github.com/mackron/miniaudio>) · [Debian](<https://tracker.debian.org/pkg/miniaudio>)
- **License:** MIT-0
- **Parsed scope:** WAV sample rate, channel and frame counts, plus first four decoded PCM samples
- **Underlying family:** miniaudio bundled dr_wav decoder
- **Local input API:** `ma_decoder_init_file; ma_decoder_get_data_format; ma_decoder_get_length_in_pcm_frames; ma_decoder_read_pcm_frames`
- **Documentation:** [API reference](<https://github.com/mackron/miniaudio/blob/0.11.26/miniaudio.h>)
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

Distinct miniaudio package and public C decoder API; WAV decoder derives from dr_wav. The C++ path uses the exact C-cell release and underlying decoder.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/cpp/miniaudio/README.md)

```sh
python3 parsarium.py build wav cpp miniaudio
python3 parsarium.py run wav cpp miniaudio controls/wav/four-samples.wav
```
