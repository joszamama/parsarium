# simplejson — JSON / Python

- **Pinned package:** `simplejson` 4.3.0 ([PyPI release and license](https://pypi.org/project/simplejson/4.3.0/), MIT OR AFL-2.1).
- **Local input API:** [`simplejson.load()`](https://simplejson.readthedocs.io/en/latest/) over a binary file-like stream; the adapter passes `BytesIO` containing local UTF-8 bytes and disables non-finite numeric extensions.
- **Valid control:** [`controls/json/structure.json`](../../../../controls/json/structure.json), a complete JSON object with nested array, number, Boolean, null, escaped newline, and Unicode escape.
- **Expected observation:** two `items`, first `id` 7, decoded first label containing a newline, `ok` true, null value, and second label `π`.
- **Underlying parser family:** simplejson's pure-Python decoder. The pinned `py3-none-any` wheel contains `decoder.py` and `scanner.py`. The [Docker receipt](../../../../projects/json/python/simplejson/verification.json) records 140 package source lines, 101 in `decoder.py`; the [AFL++ receipt](../../../../fuzzing/afl-native/json/python/simplejson/verification.json) records 159 feedback tuples. Two fixed valid controls produced 34 differing tuples in the [variant probe](../../../../data/python/json/valid-variant-feedback.json).

This is one verified API path after its control and feedback receipts pass, not a claim that the package has the most JSON-specific users. [Runnable harness](../../../../projects/json/python/simplejson/README.md).
