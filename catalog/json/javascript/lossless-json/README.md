# lossless-json — JavaScript JSON

- **Pinned release:** `lossless-json` 4.3.3, MIT; [npm tarball](https://registry.npmjs.org/lossless-json/-/lossless-json-4.3.3.tgz) and [source lock](../../../../projects/json/javascript/lossless_json/source-lock.json)
- **Adoption:** 9,738,476 npm downloads in the saved 30-day JavaScript JSON window, including transitive use
- **Local input API:** [documented `parse(text)`](https://github.com/josdejong/lossless-json/blob/v4.3.3/README.md) on strictly decoded local UTF-8 bytes
- **Family:** Own recursive-descent JSON value parser in `lib/esm/parse.js`; no underlying selected parser engine. Its source credits Tan Li Hou's parser article as an algorithmic influence.
- **Runnable target:** [Docker harness, exact controls, source coverage, and AFL++ feedback](../../../../projects/json/javascript/lossless_json/README.md)

The parser returns a nested value tree. Unlike native JavaScript `JSON.parse`, it represents every numeric token as a `LosslessNumber` holding its original spelling. The adapter reports that spelling without converting it to a JavaScript number; `-0.25e1` and `2.5e-1` therefore stay distinct from their floating-point values. Both valid controls match an independent Python JSON oracle that preserves numeric token text. The two controls do not establish support for every JSON input or duplicate-key behavior.
