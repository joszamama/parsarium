# jhove-modules — WAV / Java

- **Pinned release:** `1.20.1`
- **Upstream:** [source repository](<https://github.com/openpreserve/jhove>) · [Maven Central](<https://central.sonatype.com/artifact/org.openpreservation.jhove/jhove-modules>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/java/jhove_modules/README.md)

```sh
python3 parsarium.py build wav java jhove_modules
python3 parsarium.py run wav java jhove_modules controls/wav/256-samples.wav
```
