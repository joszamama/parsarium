# cerbero/json-parser lead check — PHP / JSON

This is a reproducible **blocked lead probe**, not a Parsarium parser project. The API and controls pass. Parser feedback does not separate the two valid controls.

The pinned 1.1.1 `JsonParser::parse($source)->lazy()` reads strings, local files and streams with the package's own byte Lexer and token-state Parser. Every nested object and array stays a `Tokens\Parser` that the same code walks. Only single key and scalar tokens reach the default `JsonDecoder`, which is `json_decode` on one token. Without `lazy()`, the eager default hands whole top-level member values to `json_decode`, so nested values then belong to the ext/json family. A lazy `Parser` does not say whether it is an object or an array, so the harness reads the Lexer's own `{`/`[` token through the public `lazyLoad()` before iterating, and checks it against the member keys.

Both valid controls give exact ordered type-tagged trees that match an independent Python `json` oracle through all three sources. The package is table-driven, though: Xdebug executes the same 294 package lines on both controls. The repository's parser-line AFL++ bridge therefore gives identical tuple ids (312 each, 15 of them proxy-only in the no-parse baseline). Xdebug 3.5 returns no branch or path data in this image. A call-count trace separates the controls only by hit-count class, which is recorded but not used as feedback.

From the repository root:

```sh
python3 lead-probes/php/json/cerbero_json_parser/check.py
```

The command builds the pinned image, which checks the source archive SHA-256 and diffs it against the Composer install. It then builds the AFL++ 4.33c bridge image from `Dockerfile.afl`. Each control and each no-parse baseline runs twice. The check fails if a tree differs from the oracle, if lazy mode passes a compound to `json_decode`, or if the bridge starts to separate the controls. It writes [the observation](../../../../data/php/json/cerbero-json-parser-lead-check.json). It does not run malformed inputs, a fuzz campaign, or vulnerability or resource tests.
