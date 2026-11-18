# openpdf-renderer — PDF / Java

- **Pinned release:** `3.0.5`
- **Upstream:** [source repository](<https://github.com/LibrePDF/OpenPDF>) · [Maven Central](<https://central.sonatype.com/artifact/com.github.librepdf/openpdf-renderer>)
- **License:** LGPL-2.1-or-later
- **Parsed scope:** PDF page count
- **Underlying family:** OpenPDF renderer (Sun PDF Renderer lineage)
- **Local input API:** `new PDFFile(ByteBuffer).getNumPages()`
- **Documentation:** [API reference](<https://github.com/LibrePDF/OpenPDF/blob/master/openpdf-renderer/src/main/java/org/openpdf/renderer/PDFFile.java>)
- **Catalog evidence:** [parser record](../../../../data/java/pdf/parsers.json) · [control verification](../../../../data/java/pdf/verification.json) · [within-ecosystem ranking](../../../../data/java/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/java/openpdf_renderer/README.md)

```sh
python3 parsarium.py build pdf java openpdf_renderer
python3 parsarium.py run pdf java openpdf_renderer controls/pdf/one-page.pdf
```
