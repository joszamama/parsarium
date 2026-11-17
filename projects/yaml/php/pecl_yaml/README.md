# pecl/yaml — YAML / PHP

Pinned release: `2.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/php/pecl-yaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml php pecl_yaml
python3 parsarium.py run yaml php pecl_yaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml php pecl_yaml CORPUS_DIR runs/yaml-pecl_yaml-replay
python3 parsarium.py afl build yaml php pecl_yaml
python3 parsarium.py afl prepare yaml php pecl_yaml runs/yaml-pecl_yaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** One run records Clang/LLVM source coverage of the yaml extension (yaml.c, parse.c, detect.c; emit.c and the headers report 0) and of source-built libyaml 0.2.5 (api.c, reader.c, scanner.c, parser.c) for one yaml_parse() call on a valid control. PHP itself is a plain build and is not covered; the PHP tree walk in summary.php runs no extension or libyaml code. AFL++ feedback comes from the native overlay: pecl/yaml yaml.c, parse.c and detect.c plus libyaml 0.2.5 reader.c, scanner.c and parser.c, instrumented through an allowlist while the same harness runs; the PHP runtime, emit.c and the rest of libyaml add no AFL++ tuples, and the full-harness maps equal the parse-only fuzz-target maps. The pinned base image does not bundle php-fuzzer; replay is per case.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
