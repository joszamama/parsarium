# github.com/mmcdole/goxpp — XML / Go

**Pilot / incomplete format cell.** This path is verified on two valid controls; the format-wide search remains bounded and incomplete.

- **Pinned release:** `v1.3.0`
- **License:** MIT
- **Parser family:** goxpp pull cursor over Go `encoding/xml.Decoder.Token()` tokenizer
- **Local input API:** `xpp.NewXMLPullParser(io.Reader, true, nil)` and `XMLPullParser.NextToken()`
- **API reference:** [Go Packages](https://pkg.go.dev/github.com/mmcdole/goxpp@v1.3.0#NewXMLPullParser)
- **Valid controls:** [catalog with namespaces](../../../../controls/xml/catalog-ns.xml) and [order with default namespace](../../../../controls/xml/order-default-ns.xml)
- **Evidence:** [parser record](../../../../data/go/xml/parsers.json), [control result](../../../../data/go/xml/verification.json), [AFL++ feedback](../../../../fuzzing/afl-native/xml/go/github_com_mmcdole_goxpp/differential.json)

The observed results include expanded element names, ordered attributes and elements, namespace declarations, text including decoded entities and CDATA, and maximum depth. The catalog control covers 84 goxpp source lines and 306 `encoding/xml` lines. Repeated AFL++ traces are identical for each valid control; the order control changes three goxpp blocks and 32 underlying tokenizer blocks. goxpp is a distinct API and state machine within the shared Go `encoding/xml` parser family.

The saved pkg.go.dev snapshot reports 132 importing packages for goxpp. This is a package adoption count, not a measure of distinct tokenizer use.

## Run

```sh
python3 parsarium.py build xml go github_com_mmcdole_goxpp
python3 parsarium.py run xml go github_com_mmcdole_goxpp controls/xml/catalog-ns.xml
python3 parsarium.py run xml go github_com_mmcdole_goxpp controls/xml/order-default-ns.xml
```
