# codecmedia — WAV / Java

- **Pinned release:** `1.2.2`
- **License:** Apache-2.0
- **Parsed scope:** parsed PCM codec, sample rate and channels
- **Underlying family:** CodecMedia RIFF/WAV parser
- **Local input API:** `CodecMedia.createDefault().probe(Path).streams()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/me/tamkungz/codecmedia/codecmedia/1.2.2/codecmedia-1.2.2-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/wav/parsers.json) · [control verification](../../../../data/java/wav/verification.json) · [within-ecosystem ranking](../../../../data/java/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "codec": "pcm",
  "sample_rate": 8000,
  "channels": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/java/codecmedia/README.md)

```sh
python3 parsarium.py build wav java codecmedia
python3 parsarium.py run wav java codecmedia controls/wav/256-samples.wav
```
