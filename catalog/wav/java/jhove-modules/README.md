# jhove-modules — WAV / Java

- **Pinned release:** `1.20.1`
- **License:** LGPL-2.1
- **Parsed scope:** WAVE identification, sample rate and channels
- **Underlying family:** JHOVE WAVE-hul module
- **Local input API:** `WaveModule.setBase(JhoveBase), parse(InputStream,RepInfo,int), getAESMetadata()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/openpreservation/jhove/jhove-modules/1.20.1/jhove-modules-1.20.1-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/wav/parsers.json) · [control verification](../../../../data/java/wav/verification.json) · [within-ecosystem ranking](../../../../data/java/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "format": "WAVE",
  "sample_rate": 8000,
  "channels": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
