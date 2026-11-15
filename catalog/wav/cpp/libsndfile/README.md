# libsndfile — WAV / C++

- **Pinned release:** `1.2.2`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** WAV sample rate, channel and frame counts, plus first four decoded PCM samples
- **Underlying family:** libsndfile WAV decoder
- **Local input API:** `sf_open(path, SFM_READ, SF_INFO); SF_FORMAT_WAV; sf_readf_short`
- **Documentation:** [API reference](<https://libsndfile.github.io/libsndfile/api.html>)
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

Own audio file parser and PCM reader. The C++ path uses the exact C-cell release and underlying decoder.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
