# ij — PNG / Java

- **Pinned release:** `1.54p`
- **Upstream:** [source repository](<https://github.com/imagej/ImageJ>) · [Maven Central](<https://central.sonatype.com/artifact/net.imagej/ij>)
- **License:** Public domain
- **Parsed scope:** RGBA pixels
- **Underlying family:** ImageJ image opener
- **Local input API:** `new ij.io.Opener().openImage(path).getBufferedImage()`
- **Documentation:** [API reference](<https://imagej.net/ij/developer/api/ij/ij/io/Opener.html>)
- **Catalog evidence:** [parser record](../../../../data/java/png/parsers.json) · [control verification](../../../../data/java/png/verification.json) · [within-ecosystem ranking](../../../../data/java/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "pixels": "ffff0000,ff00ff00"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/java/ij/README.md)

```sh
python3 parsarium.py build png java ij
python3 parsarium.py run png java ij controls/png/red-green.png
```
