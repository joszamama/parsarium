# jlayer — MP3 / Java

- **Pinned release:** `1.0.1`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** local tagged MP3 frame frequency and layer, plus ID3v2 presence
- **Underlying family:** JLayer native MP3 frame decoder with raw ID3v2 access
- **Local input API:** `new Bitstream(InputStream), readFrame(), getRawID3v2()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/javazoom/jlayer/1.0.1/jlayer-1.0.1-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3/parsers.json) · [control verification](../../../../data/java/mp3/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "frequency": 8000,
  "layer": 3,
  "id3v2_present": true
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/java/jlayer/README.md)

```sh
python3 parsarium.py build mp3 java jlayer
python3 parsarium.py run mp3 java jlayer controls/mp3/id3v2-tagged-tone.mp3
```
