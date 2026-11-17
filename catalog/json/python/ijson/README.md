# ijson — JSON / Python

**Pilot / incomplete format cell.** This path is verified on its stated controls; the format-wide search is still in progress.

- **Pinned release:** `3.6.0` (sdist `ec8f9265…45f5`; aarch64 cp311 wheel `a50ba1d5…dfa2e`)
- **License:** BSD-3-Clause AND ISC (ijson and yajl)
- **Dependencies:** none at runtime
- **Parser family:** ijson `yajl2_c` C extension over yajl 2.1.1 (`rtobar/yajl@dd88e2ea`)
- **Tested backend:** `yajl2_c`, the default when its extension imports. The pure-Python, ctypes and cffi backends are not tested.
- **Local input API:** `ijson.items(BytesIO(local JSON bytes), '')`, with exactly one root item required
- **Documentation:** [README at v3.6.0](<https://github.com/ICRAR/ijson/blob/v3.6.0/README.rst>)
- **Valid controls:** [`controls/json/structure.json`](../../../../controls/json/structure.json) and [`controls/json/nested-array.json`](../../../../controls/json/nested-array.json)
- **Catalog evidence:** [parser record](../../../../data/python/json/parsers.json) · [control result](../../../../data/python/json/verification.json) · [AFL++ feedback](../../../../data/python/json/ijson-valid-feedback.json) · [project and commands](../../../../projects/json/python/ijson/README.md)

## Observed control results

```json
{
  "root_type": "object",
  "top_level_keys": [
    "items",
    "kind"
  ],
  "item_count": 2,
  "first_id": 7,
  "first_label": "a\nb",
  "first_ok": true,
  "first_value_is_null": true,
  "second_label": "π"
}
```

```json
{
  "root_type": "array",
  "item_count": 5,
  "nested_arrays": 1,
  "nested_objects": 1
}
```

LLVM coverage reached 577 region-start lines in 21 ijson C and yajl source files on the first control. 263 of those lines are in yajl, including 92 in `yajl_parser.c`. Repeated AFL++ feedback was identical for each control and differed between the two.

The image builds the sdist at `-O0` and embeds yajl through ijson's `IJSON_EMBED_YAJL` path. Official Linux wheels link the same yajl commit as a bundled `-O3` shared library. The 46,615,664 last-month PyPI downloads cover every ijson backend and transitive installs.

## Run this target

```sh
python3 parsarium.py build json python ijson
python3 parsarium.py run json python ijson controls/json/structure.json
```
