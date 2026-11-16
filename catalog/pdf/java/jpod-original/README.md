# jpod-original — PDF / Java

- **Pinned release:** `5.6`
- **License:** BSD-3-Clause
- **Parsed scope:** PDF page count
- **Underlying family:** jPod PDF parser (original)
- **Local input API:** `PDDocument.createFromLocator(new FileLocator(File)).getPageTree().getCount()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/de/intarsys/opensource/jPod/5.6/jPod-5.6-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/pdf/parsers.json) · [control verification](../../../../data/java/pdf/verification.json) · [within-ecosystem ranking](../../../../data/java/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/java/jpod_original/README.md)

```sh
python3 parsarium.py build pdf java jpod_original
python3 parsarium.py run pdf java jpod_original controls/pdf/one-page.pdf
```
