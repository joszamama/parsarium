# mupdf — PDF / C++

- **Pinned release:** `1.28.6`
- **Upstream:** [source repository](<https://github.com/ArtifexSoftware/mupdf>) · [Debian](<https://tracker.debian.org/pkg/mupdf>)
- **License:** AGPL-3.0-or-later
- **Parsed scope:** PDF document page count
- **Underlying family:** MuPDF C document parser
- **Local input API:** `fz_open_document(fz_context*, const char* local filename); fz_count_pages(...) called from C++17`
- **Documentation:** [API reference](<https://mupdf.readthedocs.io/en/1.28.6/cookbook/c/example.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/pdf/parsers.json) · [control verification](../../../../data/cpp/pdf/verification.json) · [within-ecosystem ranking](../../../../data/cpp/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Direct MuPDF C API call from a C++17 translation unit; distinct from Poppler, PoDoFo, and qpdf. The official GitHub repository is a mirror of the canonical Ghostscript Git repository.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/cpp/mupdf/README.md)

```sh
python3 parsarium.py build pdf cpp mupdf
python3 parsarium.py run pdf cpp mupdf controls/pdf/one-page.pdf
```
