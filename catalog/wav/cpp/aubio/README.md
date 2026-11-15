# aubio — WAV / C++

- **Pinned release:** `0.4.9`
- **License:** GPL-3.0-or-later
- **Parsed scope:** WAV sample rate, channel and frame counts, plus first four decoded PCM samples
- **Underlying family:** aubio source abstraction
- **Local input API:** `new_aubio_source(local WAV path, original sample rate, hop size); aubio_source_do; aubio_source_get_samplerate, channels, duration`
- **Documentation:** [API reference](<https://github.com/aubio/aubio/blob/0.4.9/src/io/source.h>)
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

Distinct C package source API; installed build links Apple AudioToolbox and libsndfile. The exact backend chosen for this control was not isolated, so parser-engine independence is not claimed. The C++ path uses the exact C-cell release and underlying decoder.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
