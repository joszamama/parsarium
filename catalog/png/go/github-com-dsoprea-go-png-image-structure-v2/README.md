# github.com/dsoprea/go-png-image-structure/v2 — PNG / Go

- **Pinned release:** `v2.0.0-20210512210324-29b889a6093d`
- **Upstream:** [source repository](<https://github.com/dsoprea/go-png-image-structure>) · [pkg.go.dev](<https://pkg.go.dev/github.com/dsoprea/go-png-image-structure/v2>)
- **License:** MIT
- **Parsed scope:** chunks+dimensions
- **Underlying family:** PNG chunk structure parser
- **Local input API:** `PngMediaParser.ParseFile(path); ChunkDecoder.Decode(IHDR)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/dsoprea/go-png-image-structure/v2@v2.0.0-20210512210324-29b889a6093d>)
- **Catalog evidence:** [parser record](../../../../data/go/png/parsers.json) · [control verification](../../../../data/go/png/verification.json) · [within-ecosystem ranking](../../../../data/go/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "chunks": [
    "IHDR",
    "IDAT",
    "IEND"
  ],
  "height": 1,
  "width": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/go/github_com_dsoprea_go_png_image_structure_v2/README.md)

```sh
python3 parsarium.py build png go github_com_dsoprea_go_png_image_structure_v2
python3 parsarium.py run png go github_com_dsoprea_go_png_image_structure_v2 controls/png/red-green.png
```
