# metadata-extractor — WAV / Java

- **Pinned release:** `2.19.0`
- **Upstream:** [source repository](<https://github.com/drewnoakes/metadata-extractor>) · [Maven Central](<https://central.sonatype.com/artifact/com.drewnoakes/metadata-extractor>)
- **License:** Apache-2.0
- **Parsed scope:** WAV sample rate, channels and bit depth
- **Underlying family:** metadata-extractor RIFF/WAV metadata reader
- **Local input API:** `WavMetadataReader.readMetadata(File), Metadata.getFirstDirectoryOfType(WavDirectory.class)`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/drewnoakes/metadata-extractor/2.19.0/metadata-extractor-2.19.0-javadoc.jar>)
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

[Docker harness and verification receipt](../../../../projects/wav/java/metadata_extractor/README.md)

```sh
python3 parsarium.py build wav java metadata_extractor
python3 parsarium.py run wav java metadata_extractor controls/wav/256-samples.wav
```
