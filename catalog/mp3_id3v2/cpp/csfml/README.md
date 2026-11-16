# csfml — MP3 with ID3v2 / C++

- **Pinned release:** `3.0.0`
- **License:** Zlib
- **Parsed scope:** Fully decoded MP3 audio samples and stream fields from an ID3v2-tagged file; ID3v2 text is not exposed
- **Underlying family:** CSFML wrapper over SFML SoundFileReaderMp3/minimp3
- **Local input API:** `sfSoundBuffer_createFromFile(local filename); sfSoundBuffer_getSampleCount/getSampleRate/getChannelCount/getSamples`
- **Documentation:** [API reference](<https://github.com/SFML/CSFML/blob/3.0.0/include/CSFML/Audio/SoundBuffer.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp3_id3v2/parsers.json) · [control verification](../../../../data/cpp/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "samples": 8000,
  "sample_rate": 8000,
  "channels": 1
}
```

The CSFML C API delegates to the SFML C++ audio core, using its SoundFileReaderMp3 and bundled minimp3. C and C++ CSFML calls share the same library, and SFML is also counted separately in C++ as a distinct upstream package/API wrapper relation.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/cpp/csfml/README.md)

```sh
python3 parsarium.py build mp3_id3v2 cpp csfml
python3 parsarium.py run mp3_id3v2 cpp csfml controls/mp3_id3v2/tone-tags.mp3
```
