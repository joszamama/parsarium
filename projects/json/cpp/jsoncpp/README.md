# JsonCpp — JSON / C++

Pinned release: `1.9.8` (source tarball SHA-256 `51828cf3…d904`, [source lock](source-lock.json)). [Manifest](manifest.json) · [verification receipt](verification.json)

The harness passes local bytes to the documented range API `Json::CharReaderBuilder::newCharReader()->parse(begin, end, &root, &errors)` ([reader.h](https://github.com/open-source-parsers/jsoncpp/blob/1.9.8/include/json/reader.h)) with `CharReaderBuilder::strictMode`. It walks the resulting `Json::Value` tree and reports the root kind, sorted top-level keys, all strings and numbers, and counts of objects, arrays, booleans, nulls and the container depth.

| Control | Result |
| --- | --- |
| `controls/json/nested-object.json` | object root, 7 keys, 5 objects, 3 arrays, 5 strings (incl. `café "quoted"`), 5 numbers, 2 booleans, 1 null, depth 4; 810 JsonCpp lines covered, 435 in `json_reader.cpp` |
| `controls/json/nested-array.json` | array root, 2 objects, 4 arrays, strings `A` and `two`, numbers 0.25 and 1, depth 3 |

AFL++ 4.33c overlay: 1,036 edges on the first control. Each control traced twice gives identical AFL++ tuples and covered lines; the two controls differ by 90 tuples and 21 JsonCpp source lines ([differential receipt](../../../../fuzzing/afl-native/json/cpp/jsoncpp/differential.json)).

Selection evidence: [data/cpp/json](../../../../data/cpp/json/ranking.md).

## Run from the repository root

```sh
python3 parsarium.py build json cpp jsoncpp
python3 parsarium.py run json cpp jsoncpp controls/json/nested-object.json
python3 parsarium.py replay json cpp jsoncpp CORPUS_DIR runs/json-jsoncpp-replay
python3 parsarium.py afl build json cpp jsoncpp
python3 parsarium.py afl prepare json cpp jsoncpp runs/json-jsoncpp-afl
python3 scripts/verify_cpp_json_feedback.py
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
