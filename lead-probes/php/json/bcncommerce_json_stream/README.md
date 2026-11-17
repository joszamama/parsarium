# bcncommerce/json-stream lead check — PHP / JSON

This is a reproducible **excluded lead probe**, not a Parsarium parser project.

The pinned 0.4.2 release (source repository skolodyazhnyy/json-stream) documents a `Reader` over a stream resource. `Reader::read()` returns PHP arrays for objects as well as lists, so an empty object and an empty array come back the same, and its tokenizer casts every number with `floatval`. Neither valid control matches the independent Python `json` oracle: `{}` becomes an empty list and `1` becomes `1.0`. Xdebug also executes the same 143 `Reader`/`Tokenizer` lines on both controls, so there is no input-dependent line feedback to bridge. The package's event `Parser.php` is a copy of the salsify/jsonstreamingparser state machine (the same `STATE_*` constants), a family already selected.

From the repository root:

```sh
python3 lead-probes/php/json/tree_line_lead_check.py bcncommerce_json_stream
```

The command builds the pinned image, which checks the source archive SHA-256 and diffs it against the Composer install. It runs each valid control twice and writes [the observation](../../../../data/php/json/bcncommerce-json-stream-lead-check.json). It does not run malformed inputs, a fuzz campaign, or vulnerability or resource tests.
