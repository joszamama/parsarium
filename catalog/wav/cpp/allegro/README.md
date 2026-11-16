# allegro — WAV / C++

- **Pinned release:** `5.2.11.3`
- **License:** Zlib
- **Parsed scope:** WAV sample rate, channel and frame counts, plus first four decoded PCM samples
- **Underlying family:** Allegro audio codec WAV loader
- **Local input API:** `al_init; al_install_audio; al_init_acodec_addon; al_load_sample(local WAV path); al_get_sample_frequency, channels, length, data`
- **Documentation:** [API reference](<https://liballeg.org/a5docs/5.2.11.3/acodec.html>)
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

Allegro audio codec add-on registers its own WAV loader; official versioned docs list little-endian PCM WAV support. Core, audio and codec add-on binaries are SHA-256-checked. The C++ path uses the exact C-cell release and underlying decoder.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/cpp/allegro/README.md)

```sh
python3 parsarium.py build wav cpp allegro
python3 parsarium.py run wav cpp allegro controls/wav/four-samples.wav
```
