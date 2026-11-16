# jdsp — WAV / Java

- **Pinned release:** `3.1.1`
- **License:** MIT
- **Parsed scope:** sample rate, channels and frame count
- **Underlying family:** JDSP WAV API over wavfile
- **Local input API:** `new WAV().readWAV(String localPath), getProperties()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/github/psambit9791/jdsp/3.1.1/jdsp-3.1.1-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/wav/parsers.json) · [control verification](../../../../data/java/wav/verification.json) · [within-ecosystem ranking](../../../../data/java/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "frames": 256
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/java/jdsp/README.md)

```sh
python3 parsarium.py build wav java jdsp
python3 parsarium.py run wav java jdsp controls/wav/256-samples.wav
```
