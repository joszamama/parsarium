# github.com/antchfx/xmlquery — XML / Go

**Pilot / incomplete format cell.** This path is verified on the stated valid controls; format-wide search continues.

- **Pinned release:** `v1.5.2` (Go module archive SHA-256 `cdb7830a6e1e3f52c3d3a084b55b4bdf84f73b8073c582bca8f5f00d15a5f94c`)
- **License:** MIT, present as `LICENSE` in the pinned Go module archive (SHA-256 `c181eed254a608399a1059ddf5cb72cb1f1a5841a083aaa30f3e6713853ddf9f`)
- **Parser family:** xmlquery DOM over Go `encoding/xml.Decoder.Token()` tokenizer. The tokenizer is shared with etree and the standard API, while xmlquery constructs its own DOM.
- **Local input API:** `xmlquery.Parse(io.Reader)` returns a `*Node`; the harness walks child and sibling links and observes names, attributes, and text.
- **Documentation:** [API reference](https://pkg.go.dev/github.com/antchfx/xmlquery@v1.5.2#Parse) · [tagged source](https://github.com/antchfx/xmlquery/tree/v1.5.2)
- **Valid controls:** [`catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml) and [`order-default-ns.xml`](../../../../controls/xml/order-default-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/go/xml/parsers.json) · [control result](../../../../data/go/xml/verification.json)

The first control parses a prefixed root, default namespace, prefixed attribute, entity references, and CDATA. The second parses namespace reset, processing instruction, character references, and quoted attribute text. The harness requires an exact canonical structure summary for each. Source coverage counts only xmlquery and its `encoding/xml` dependency; the AFL++ feedback bridge maps xmlquery source blocks.

## Run this target

```sh
python3 parsarium.py build xml go github_com_antchfx_xmlquery
python3 parsarium.py run xml go github_com_antchfx_xmlquery controls/xml/catalog-ns.xml
python3 parsarium.py afl build xml go github_com_antchfx_xmlquery
python3 parsarium.py afl prepare xml go github_com_antchfx_xmlquery runs/xmlquery-afl
```
