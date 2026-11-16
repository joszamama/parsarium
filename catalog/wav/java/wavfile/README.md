# wavfile — WAV / Java

- **Pinned release:** `1.0.0`
- **License:** MIT
- **Parsed scope:** sample rate, channels, frame count and four PCM samples
- **Underlying family:** wavfile Java WAV reader
- **Local input API:** `WavFile.openWavFile(File), readFrames(int[],int)`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/github/psambit9791/wavfile/1.0.0/wavfile-1.0.0-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/wav/parsers.json) · [control verification](../../../../data/java/wav/verification.json) · [within-ecosystem ranking](../../../../data/java/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "frames": 256,
  "samples": [
    0,
    1000,
    -1000,
    0
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/java/wavfile/README.md)

```sh
python3 parsarium.py build wav java wavfile
python3 parsarium.py run wav java wavfile controls/wav/256-samples.wav
```
