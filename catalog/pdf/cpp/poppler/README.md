# poppler — PDF / C++

- **Pinned release:** `26.11.0`
- **License:** GPL-2.0-only OR GPL-3.0-only
- **Parsed scope:** PDF document page count
- **Underlying family:** Poppler PDF parser, C++ frontend
- **Local input API:** `poppler::document::load_from_file(const std::string&) on a local PDF path; pages()`
- **Documentation:** [API reference](<https://poppler.freedesktop.org/api/cpp/classpoppler_1_1document.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/pdf/parsers.json) · [control verification](../../../../data/cpp/pdf/verification.json) · [within-ecosystem ranking](../../../../data/cpp/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Native Poppler C++ frontend over Poppler core; its other frontends share the same parser engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/cpp/poppler/README.md)

```sh
python3 parsarium.py build pdf cpp poppler
python3 parsarium.py run pdf cpp poppler controls/pdf/one-page.pdf
```
