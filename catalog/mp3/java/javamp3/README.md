# javamp3 — MP3 / Java

- **Pinned release:** `1.0.1`
- **Upstream:** [source repository](<https://github.com/delthas/JavaMP3>) · [Maven Central](<https://central.sonatype.com/artifact/fr.delthas/javamp3>)
- **License:** MIT
- **Parsed scope:** 44.1 kHz tagged MP3 sample rate, channel mode and 32 decoded PCM bytes
- **Underlying family:** JavaMP3 native MPEG audio decoder
- **Local input API:** `new Sound(BufferedInputStream localMp3), getSamplingFrequency(), isStereo(), read(byte[])`
- **Documentation:** [API reference](<https://github.com/delthas/JavaMP3>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3/parsers.json) · [control verification](../../../../data/java/mp3/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone-44k.mp3`](../../../../controls/mp3/id3v2-tagged-tone-44k.mp3)

## Observed control result

```json
{
  "frequency": 44100,
  "stereo": false,
  "sample_bytes": 32
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/java/javamp3/README.md)

```sh
python3 parsarium.py build mp3 java javamp3
python3 parsarium.py run mp3 java javamp3 controls/mp3/id3v2-tagged-tone-44k.mp3
```
