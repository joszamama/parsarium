# symfony/json-streamer lead check — PHP / JSON

This is a reproducible **excluded lead probe**, not a Parsarium parser project.

`JsonStreamReader::read($input, Type $type)` in the pinned v8.1.10 release is type-directed: it generates PHP reader code for the declared type. For a schema-free tree the type is `Type::mixed()`, and the generated reader is a single `Decoder::decodeStream()` call, which is `json_decode` with associative arrays. Both valid controls therefore come from ext/json, and the empty object and empty array of each control are indistinguishable. Xdebug executes the same 129 package lines (code generation, metadata loading and dispatch) on both controls. The package's own `Splitter` only cuts member boundaries when a typed collection is declared, and those member values still go through `json_decode`.

From the repository root:

```sh
python3 lead-probes/php/json/tree_line_lead_check.py symfony_json_streamer
```

The command builds the pinned image, which checks the source archive SHA-256 and diffs it against the Composer install. It runs each valid control twice and writes [the observation](../../../../data/php/json/symfony-json-streamer-lead-check.json), including the generated reader. It does not run malformed inputs, a fuzz campaign, or vulnerability or resource tests.
