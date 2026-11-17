# jsoncons 1.10.0 — C++ / JSON candidate

The documented `jsoncons::json::parse(const char*, size_t)` consumes local bytes and constructs a JSON value tree. The replay dumps that parsed tree. The two valid controls are compared with an independent typed JSON oracle so object, array, integer, floating point, string, Boolean, and null values remain distinct.

The pinned jsoncons release is header-only under the Boost Software License 1.0. The base Docker replay records line coverage in its own `json_parser.hpp`. A separate probe calls only `json::parse`, and its AFL++ build allowlists that parser header; tree serialization and the harness do not contribute to the feedback map. The [differential receipt](../../../../fuzzing/afl-native/json/cpp/jsoncons/differential.json) records repeated maps for both valid controls.

From the repository root:

```sh
python3 parsarium.py build json cpp jsoncons
python3 parsarium.py run json cpp jsoncons controls/json/nested-object.json
python3 parsarium.py afl build json cpp jsoncons
python3 parsarium.py afl prepare json cpp jsoncons runs/json-jsoncons-afl
```

The dedicated Debian `libjsoncons-dev` package had 3 installations in the saved popcon snapshot. This is a comparable but very small adoption signal. jsoncons also supports other data formats; the harness verifies its JSON parser only. This candidate is separate from the selected C++ JSON catalog pending curation.
