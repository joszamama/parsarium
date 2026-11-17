# colinodell/json5 lead check — PHP / JSON

This is a reproducible **excluded lead probe**, not a Parsarium parser project. The pinned v3.0.0 `Json5Decoder::decode(string)` and `json5_decode(string)` APIs call PHP's `json_decode` first and return its result when it succeeds. The package's own JSON5 parser is private and runs only after ext/json rejects the input. Valid RFC 8259 JSON therefore never reaches package parser code, and this route shares the ext/json family already verified as `json/php/stdlib_json_decode`.

From the repository root:

```sh
python3 lead-probes/php/json/colinodell_json5/check.py
```

The command builds the pinned Docker image, which checks the source archive SHA-256 and diffs it against the Composer install. It then decodes both valid controls through both APIs under Xdebug and compares exact type-tagged trees with an independent Python `json` oracle. It fails if any line of the constructor, the JSON5 fallback or the private parser methods runs. It writes [the observation](../../../../data/php/json/colinodell-json5-lead-check.json). It does not run JSON5-only or malformed inputs, a fuzz campaign or an AFL++ bridge: a bridge scoped to package parser lines would have no parser features on valid JSON.
