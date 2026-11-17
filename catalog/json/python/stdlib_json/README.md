# CPython `json` — JSON / Python standard library

- **Pinned runtime:** CPython 3.14.4 in the container. Its `json/decoder.py`, `json/scanner.py`, and `json/__init__.py` are checked by SHA-256.
- **Official input API:** [`json.load()`](https://docs.python.org/3.14/library/json.html) on a local binary file-like object. The harness passes a decoder class that selects CPython's pure-Python scanner and rejects non-finite numeric extensions.
- **Valid control:** [`structure.json`](../../../../controls/json/structure.json), with nested structure, escaped newline, Unicode escape, number, Boolean, and null.
- **Expected observation:** two `items`, first `id` 7, a decoded newline in its label, `ok` true, null value, and second label `π`.
- **Coverage scope:** CPython's pure-Python JSON decoder and scanner source. The default built-in `_json` accelerator is outside this harness's coverage and AFL feedback claim.
- **Fixed valid-input feedback check:** [`structure.json`](../../../../controls/json/structure.json) and [`one-item.json`](../../../../controls/json/one-item.json) exercise 166 and 141 parser-source line features, respectively. Their AFL maps contain 186 and 161 edge IDs, with 25 different IDs. [Probe](../../../../data/python/json/probe-stdlib-valid-feedback.py) · [result](../../../../data/python/json/stdlib-valid-variant-feedback.json). No mutation campaign is involved.

This standard API is separate from third-party package popularity. [Runnable harness](../../../../projects/json/python/stdlib_json/README.md).
