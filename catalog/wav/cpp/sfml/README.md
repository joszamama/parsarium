# sfml — WAV / C++

- **Pinned release:** `3.0.2`
- **Upstream:** [source repository](<https://github.com/SFML/SFML>)
- **License:** Zlib
- **Parsed scope:** WAV sample rate, channels, frame count and four decoded PCM samples
- **Underlying family:** SFML audio sound-file decoder
- **Local input API:** `sf::SoundBuffer::loadFromFile; getSampleRate; getChannelCount; getSampleCount; getSamples`
- **Documentation:** [API reference](<https://github.com/SFML/SFML/blob/3.0.2/include/SFML/Audio/SoundBuffer.hpp>)
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

Native C++ sound buffer API; CSFML is its C facade and shares the SFML underlying parser family.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/cpp/sfml/README.md)

```sh
python3 parsarium.py build wav cpp sfml
python3 parsarium.py run wav cpp sfml controls/wav/four-samples.wav
```
