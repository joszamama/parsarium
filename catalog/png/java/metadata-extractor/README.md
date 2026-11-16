# metadata-extractor — PNG / Java

- **Pinned release:** `2.22.0`
- **License:** Apache-2.0
- **Parsed scope:** PNG dimensions
- **Underlying family:** metadata-extractor PNG chunk reader
- **Local input API:** `ImageMetadataReader.readMetadata(File); PngDirectory IHDR width/height`
- **Documentation:** [API reference](<https://github.com/drewnoakes/metadata-extractor>)
- **Catalog evidence:** [parser record](../../../../data/java/png/parsers.json) · [control verification](../../../../data/java/png/verification.json) · [within-ecosystem ranking](../../../../data/java/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/java/metadata_extractor/README.md)

```sh
python3 parsarium.py build png java metadata_extractor
python3 parsarium.py run png java metadata_extractor controls/png/red-green.png
```
