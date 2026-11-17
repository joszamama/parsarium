# Glaze — JSON / C++

Pinned release: `9.1.0` (MIT). [Manifest](manifest.json) · [source lock](source-lock.json) · [verification receipt](verification.json)

`glz::read_json(glz::generic_i64&, std::string)` reads a local byte-backed string into Glaze's ordered generic DOM. The controls verify nested object and array roots, key order, UTF-8 strings, escapes, booleans, null, signed integers, and floating values. The replay serializes the parsed DOM and checks exact tree structure and number kinds against both valid control files. [Parser record](../../../../data/cpp/json/parsers.json)

Glaze is rank 5 among the five C++ JSON packages with comparable Debian source-package adoption values: 171 `sourcemax/by_inst` installations, equal to its `libglaze-dev` count. Boost.JSON remains separate and primary-unranked because its Debian source covers all of Boost. Glaze has its own JSON reader in `include/glaze/json/read.hpp`. [Cell ranking](../../../../data/cpp/json/ranking.md)

The Docker build instruments Glaze's own headers for LLVM source coverage. Its [parser-only AFL++ probe](parser-probe.cpp) calls `read_json` without serializing or walking the DOM. The two valid controls produce repeatable, input-dependent parser feedback. [Feedback receipt](../../../../fuzzing/afl-native/json/cpp/glaze/differential.json)

## Run from the repository root

```sh
python3 parsarium.py build json cpp glaze
python3 parsarium.py run json cpp glaze controls/json/nested-object.json
python3 parsarium.py run json cpp glaze controls/json/nested-array.json
python3 parsarium.py replay json cpp glaze CORPUS_DIR runs/json-glaze-replay
python3 parsarium.py afl build json cpp glaze
python3 parsarium.py afl prepare json cpp glaze runs/json-glaze-afl
python3 projects/json/cpp/glaze/verify-parser-feedback.py
```

`CORPUS_DIR` is a directory of JSON files. AFL++ preparation creates a seeded plan but does not start a campaign. The valid controls do not establish complete RFC 8259, malformed-input, numeric-limit, or all Unicode behavior.
