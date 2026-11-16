# scireum-jpod — PDF / Java

- **Pinned release:** `2.0`
- **License:** BSD-3-Clause
- **Parsed scope:** PDF page count
- **Underlying family:** jPod PDF parser (Scireum fork)
- **Local input API:** `PDDocument.createFromLocator(new FileLocator(File)).getPageTree().getCount()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/scireum/jpod/2.0/jpod-2.0-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/pdf/parsers.json) · [control verification](../../../../data/java/pdf/verification.json) · [within-ecosystem ranking](../../../../data/java/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/java/scireum_jpod/README.md)

```sh
python3 parsarium.py build pdf java scireum_jpod
python3 parsarium.py run pdf java scireum_jpod controls/pdf/one-page.pdf
```
