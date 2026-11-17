# Glaze — JSON / C++

- **Pinned release:** `9.1.0`, MIT
- **Local input API:** `glz::read_json(glz::generic_i64&, std::string)` ([pinned documentation](https://github.com/stephenberry/glaze/blob/v9.1.0/docs/generic-json.md))
- **Parser family:** Glaze's own template-based JSON reader
- **Valid controls:** [nested object](../../../../controls/json/nested-object.json), [nested array](../../../../controls/json/nested-array.json)
- **Adoption:** 171 Debian source-package installations and 171 `libglaze-dev` installations in the recorded snapshot; rank 5 among comparable C++ JSON packages. [Ranking and limits](../../../../data/cpp/json/ranking.md)
- **Evidence:** [parser record](../../../../data/cpp/json/parsers.json), [control result](../../../../data/cpp/json/verification.json), [parser-only AFL++ feedback](../../../../fuzzing/afl-native/json/cpp/glaze/differential.json)

The [runnable project](../../../../projects/json/cpp/glaze/README.md) contains the pinned Docker build, local-buffer harness, source-coverage check, and AFL++ target.
