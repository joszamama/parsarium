# jcodec — WAV / Java

- **Pinned release:** `0.2.5`
- **License:** BSD-2-Clause
- **Parsed scope:** WAV sample rate, channels and bit depth
- **Underlying family:** JCodec WAV demuxer
- **Local input API:** `new WavInput.WavFile(File).getFormat()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/jcodec/jcodec/0.2.5/jcodec-0.2.5-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/wav/parsers.json) · [control verification](../../../../data/java/wav/verification.json) · [within-ecosystem ranking](../../../../data/java/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "bits": 16
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/java/jcodec/README.md)

```sh
python3 parsarium.py build wav java jcodec
python3 parsarium.py run wav java jcodec controls/wav/256-samples.wav
```
