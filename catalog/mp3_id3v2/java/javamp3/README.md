# javamp3 — MP3 with ID3v2 / Java

- **Pinned release:** `1.0.1`
- **License:** MIT
- **Parsed scope:** 44.1 kHz tagged MP3 sample rate, channel mode and 32 decoded PCM bytes
- **Underlying family:** JavaMP3 native MPEG audio decoder
- **Local input API:** `new Sound(BufferedInputStream localMp3), getSamplingFrequency(), isStereo(), read(byte[])`
- **Documentation:** [API reference](<https://github.com/delthas/JavaMP3>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3_id3v2/parsers.json) · [control verification](../../../../data/java/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags-44k.mp3`](../../../../controls/mp3_id3v2/tone-tags-44k.mp3)

## Observed control result

```json
{
  "frequency": 44100,
  "stereo": false,
  "sample_bytes": 32
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
