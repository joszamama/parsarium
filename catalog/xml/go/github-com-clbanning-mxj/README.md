# github.com/clbanning/mxj — XML / Go

**Pilot / incomplete format cell.** This path is verified on the stated valid controls; format-wide search continues.

- **Pinned release:** `v1.8.4` (Go module archive SHA-256 `8947cf617bdd9efc62817c8ddb17bafe497f35abdf10a3c60f295e387f633f70`, tag commit `b0d71e6effe1addc982453290a91f15ba0a50922`)
- **License:** MIT, with the Go Authors' BSD-3-Clause notice, both in `LICENSE` in the pinned Go module archive (SHA-256 `b8eff858879438dbaefa6f153553230337c4776a861b8d658f295636a88050ec`)
- **Parser family:** mxj map conversion over Go `encoding/xml.Decoder.Token()`. The tokenizer is shared with etree, xmlquery and the standard API; mxj builds only the map. It is not an independent tokenizer.
- **Local input API:** `mxj.NewMapXml([]byte)` and `mxj.NewMapXmlReader(io.Reader)` each return an `mxj.Map`. The harness calls both and requires the two maps to agree.
- **Adoption metric:** 553 pkg.go.dev Imported by packages for the v1 module path, captured 2026-11-17 ([snapshot](../../../../data/go/xml/registry-snapshot.json)). The v2 path (178) is a separate lead and is not added. Importers may use mxj for JSON or map work rather than XML.
- **Documentation:** [API reference](https://pkg.go.dev/github.com/clbanning/mxj@v1.8.4#NewMapXml) · [tagged source](https://github.com/clbanning/mxj/tree/v1.8.4)
- **Valid controls:** [`catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml) and [`order-default-ns.xml`](../../../../controls/xml/order-default-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/go/xml/parsers.json) · [control result](../../../../data/go/xml/verification.json)

The harness reports map paths built from local names and list indexes, `-`-prefixed attribute keys, `#text` and simple string values, empty elements, list lengths and depth. Each control must match an exact summary. On the first control mxj keeps both `item` siblings in order, puts `Café & té` beside attributes as `#text`, and decodes the entity references and CDATA. On the second it keeps the character references, maps `<leaf/>` to an empty string, and keeps `xmlns=""` as an attribute.

The map loses namespace URIs and prefixes (`c:catalog` becomes `catalog`, `p:amount` becomes `amount`). Namespace declarations become ordinary attributes (`-xmlns`, `-c`, `-p`), so a declaration and an attribute with the same local name collide. Order between differently named siblings, comments, processing instructions, the XML declaration, and mixed-content runs are dropped. Leading and trailing whitespace in text is trimmed. None of these are claimed.

Source coverage counts mxj and its `encoding/xml` dependency. All 65 covered mxj lines are in `xml.go`. The AFL++ bridge maps only mxj source blocks. The repeated control gives identical feedback; the second control changes 2 of 48 blocks, the `#text` branch and the empty-element branch of `xmlToMapParser`. That difference is real but narrow.

## Run this target

```sh
python3 parsarium.py build xml go github_com_clbanning_mxj
python3 parsarium.py run xml go github_com_clbanning_mxj controls/xml/catalog-ns.xml
python3 parsarium.py afl build xml go github_com_clbanning_mxj
python3 parsarium.py afl prepare xml go github_com_clbanning_mxj runs/mxj-afl
```
