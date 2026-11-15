# libreofficekit — PDF / C

- **Pinned release:** `26.8.3.1`
- **License:** MPL-2.0
- **Parsed scope:** PDF imported as a two-page Draw document through C LibreOfficeKit
- **Underlying family:** LibreOffice PDF import through LibreOfficeKit C ABI
- **Local input API:** `lok_init_2(pinned local app Frameworks, local profile URI); documentLoad(file:// local PDF path); getDocumentType(); getParts()`
- **Documentation:** [API reference](<https://github.com/LibreOffice/core/blob/libreoffice-26.8.3.1/include/LibreOfficeKit/LibreOfficeKitInit.h>)
- **Catalog evidence:** [parser record](../../../../data/c/pdf/parsers.json) · [control verification](../../../../data/c/pdf/verification.json) · [within-ecosystem ranking](../../../../data/c/pdf/ranking.md)
- **Valid control:** [`controls/pdf/two-page.pdf`](../../../../controls/pdf/two-page.pdf)

## Observed control result

```json
{
  "type": "drawing",
  "pages": 2
}
```

The installed package bundles xpdfimport with Poppler markers; the exact PDF import execution path was not traced. It is a distinct open-source package API but independence from Poppler/PDFium syntax engines is unestablished.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
