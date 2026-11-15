# sfml — MP3 with ID3v2 / C++

- **Pinned release:** `3.0.2`
- **License:** Zlib
- **Parsed scope:** MP3 audio sample count and one decoded sample from an ID3v2-tagged file; ID3v2 text is not exposed
- **Underlying family:** SFML SoundFileReaderMp3 over bundled minimp3
- **Local input API:** `sf::InputSoundFile::openFromFile(local filename); getSampleCount/getSampleRate/getChannelCount; read decoded sample`
- **Documentation:** [API reference](<https://www.sfml-dev.org/documentation/3.0.2/classsf_1_1InputSoundFile.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp3_id3v2/parsers.json) · [control verification](../../../../data/cpp/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "samples": 8000,
  "sample_rate": 8000,
  "channels": 1,
  "decoded_samples": 1
}
```

The pinned SFML SoundFileReaderMp3.cpp uses bundled minimp3. CSFML 3.0.0 is a separate package wrapper over this same SFML engine; both C++ rows share the decoder family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
