# ujson — JSON / Python

**Pilot / incomplete format cell.** This path is verified on its stated controls; the format-wide search is still in progress.

- **Pinned release:** `6.1.0` (sdist `aef7ea4c…0c29`; aarch64 cp311 wheel `716d2c90…87fd6`; upstream tag commit `ec958a17`)
- **License:** BSD-3-Clause AND TCL (ujson); vendored double-conversion is BSD-3-Clause
- **Dependencies:** none at runtime
- **Parser family:** UltraJSON C decoder (`decode.c`), with vendored double-conversion 3.2.0 C++ for numbers with a fraction or exponent
- **Local input API:** `ujson.loads(local JSON bytes)`; `ujson.loads(str)` gives the same tree on both controls
- **Documentation:** [README at 6.1.0](<https://github.com/ultrajson/ultrajson/blob/6.1.0/README.md#usage>)
- **Valid controls:** [`controls/json/structure.json`](../../../../controls/json/structure.json) and [`controls/json/nested-array.json`](../../../../controls/json/nested-array.json)
- **Catalog evidence:** [parser record](../../../../data/python/json/parsers.json) · [control result](../../../../data/python/json/verification.json) · [oracle and AFL++ feedback](../../../../data/python/json/ujson-valid-feedback.json) · [project and commands](../../../../projects/json/python/ujson/README.md)

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

On both controls, `ujson.loads` on bytes and on text returned the same type-tagged tree as CPython 3.11.2 `json.loads`. The check compares member order, int against float, and floats by `float.hex`. The oracle ran under `python3 -I` in the same image, where ujson is not importable.

LLVM coverage reached 266 region-start lines in 9 ujson source files on the first control. 155 of those lines are in `decode.c` and 86 are in double-conversion. `encode.c` did not run. Repeated AFL++ feedback was identical for each control. The two controls differed by 67 source features (26 in `decode.c`, 41 in double-conversion) and 68 AFL++ tuples.

The controls contain no duplicate keys, no large or inexact numbers, and no `NaN` or `Infinity` tokens. Per the pinned source, duplicate keys keep the last value, integer overflow falls back to arbitrary-precision `int`, and `NaN`, `Infinity` and `-Infinity` are accepted. None of this was tested.

The image builds the sdist at `-O0` without stripping. The official wheel is one optimised, stripped extension built from the same sources. The 29,543,889 last-month PyPI downloads include encoder-only use and transitive installs.

## Run this target

```sh
python3 parsarium.py build json python ujson
python3 parsarium.py run json python ujson controls/json/structure.json
```
