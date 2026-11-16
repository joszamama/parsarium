# sambox — PDF / Java

- **Pinned release:** `4.0.0.M8`
- **License:** Apache-2.0
- **Parsed scope:** PDF page count
- **Underlying family:** SAMBox (PDFBox fork)
- **Local input API:** `PDFParser.parse(SeekableSources.seekableSourceFrom(File)).getNumberOfPages()`
- **Documentation:** [API reference](<https://github.com/torakiki/sambox>)
- **Catalog evidence:** [parser record](../../../../data/java/pdf/parsers.json) · [control verification](../../../../data/java/pdf/verification.json) · [within-ecosystem ranking](../../../../data/java/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/java/sambox/README.md)

```sh
python3 parsarium.py build pdf java sambox
python3 parsarium.py run pdf java sambox controls/pdf/one-page.pdf
```
