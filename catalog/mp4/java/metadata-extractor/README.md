# metadata-extractor — MP4 / Java

- **Pinned release:** `2.22.0`
- **License:** Apache-2.0
- **Parsed scope:** parsed video width and height
- **Underlying family:** metadata-extractor MP4 box reader
- **Local input API:** `Mp4MetadataReader.readMetadata(File localMp4), Mp4VideoDirectory TAG_WIDTH and TAG_HEIGHT`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/drewnoakes/metadata-extractor/2.22.0/metadata-extractor-2.22.0-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp4/parsers.json) · [control verification](../../../../data/java/mp4/verification.json) · [within-ecosystem ranking](../../../../data/java/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "width": 2,
  "height": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/java/metadata_extractor/README.md)

```sh
python3 parsarium.py build mp4 java metadata_extractor
python3 parsarium.py run mp4 java metadata_extractor controls/mp4/red-av.mp4
```
