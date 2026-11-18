# atril — PDF / C

- **Pinned release:** `1.28.2`
- **Upstream:** [source repository](<https://github.com/mate-desktop/atril>) · [Debian](<https://tracker.debian.org/pkg/atril>)
- **License:** GPL-2.0-or-later
- **Parsed scope:** PDF page count through Atril libdocument C API
- **Underlying family:** Atril PDF backend over Poppler GLib
- **Local input API:** `ev_init(); g_filename_to_uri(local path); ev_document_factory_get_document(uri, error); ev_document_get_n_pages(document)`
- **Documentation:** [API reference](<https://github.com/mate-desktop/atril/blob/v1.28.2/libdocument/ev-document-factory.h>)
- **Catalog evidence:** [parser record](../../../../data/c/pdf/parsers.json) · [control verification](../../../../data/c/pdf/verification.json) · [within-ecosystem ranking](../../../../data/c/pdf/ranking.md)
- **Valid control:** [`controls/pdf/two-page.pdf`](../../../../controls/pdf/two-page.pdf)

## Observed control result

```json
{
  "pages": 2
}
```

Atril is an Evince-derived package with a documented local URI factory and its own PDF backend, but the backend calls Poppler GLib/core for PDF syntax. The verified Docker build uses the official 1.28.2 release tarball; the catalog uses the same tag archive, and pinned API/backend source members have matching SHA-256 values across both archives. The route adds a package API, not an independent parser engine. Its Debian adoption signal is supplemental and not directly comparable with Homebrew requested-install counts.

The verified Docker harness disables LeakSanitizer because Atril's URI factory retains a 16-byte GLib MIME allocation on the valid control. AddressSanitizer and UndefinedBehaviorSanitizer remain enabled. The project-local source lock pins the official release tarball and checks catalog API/backend members against the tag archive.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/c/atril/README.md)

```sh
python3 parsarium.py build pdf c atril
python3 parsarium.py run pdf c atril controls/pdf/two-page.pdf
```
