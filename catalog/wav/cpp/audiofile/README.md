# audiofile — WAV / C++

- **Pinned release:** `1.1.4`
- **License:** MIT
- **Parsed scope:** WAV sample rate, channels, frame count and four decoded PCM samples
- **Underlying family:** adamstark AudioFile WAV parser
- **Local input API:** `AudioFile<int16_t>::load(const std::string&) or loadFromMemory(const std::vector<uint8_t>&); getSampleRate; getNumChannels; getNumSamplesPerChannel; samples`
- **Documentation:** [API reference](<https://github.com/adamstark/AudioFile/blob/1.1.4/README.md>)
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

Header-only C++ WAV parser; unrelated to the C Audio File Library package called libaudiofile.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/cpp/audiofile/README.md)

```sh
python3 parsarium.py build wav cpp audiofile
python3 parsarium.py run wav cpp audiofile controls/wav/four-samples.wav
```
