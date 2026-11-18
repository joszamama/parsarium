# gsoap — XML / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.8.142`
- **Upstream:** [Debian](<https://tracker.debian.org/pkg/gsoap>)
- **License:** GPL-2.0
- **Parser family:** gSOAP own XML engine (stdsoap2.cpp tokenizer and namespace stack) with its DOM parser (dom.cpp)
- **Local input API:** `xsd__anyType dom(ctx) with ctx = soap_new1(SOAP_C_UTFSTRING | SOAP_DOM_TREE), then std::istream >> dom over a std::istringstream of the local bytes and a check of ctx->error; the DOM is walked through soap_dom_element (name, nstr, atts, elts, text) and soap_dom_attribute (name, nstr, text); soap_destroy/soap_end/soap_free`
- **Documentation:** [API reference](<https://www.genivia.com/doc/dom/html/index.html>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/cpp/xml/parsers.json) · [control result](../../../../data/cpp/xml/verification.json)

## Observed control result

```json
{
  "attributes": [
    "version=1",
    "id=a1",
    "{urn:parsarium:catalog}lang=es",
    "id=b2"
  ],
  "elements": [
    "{urn:parsarium:catalog}catalog",
    "{urn:parsarium:item}item",
    "{urn:parsarium:item}item",
    "{urn:parsarium:item}name",
    "{urn:parsarium:item}note"
  ],
  "max_depth": 3,
  "namespace_declarations": 2,
  "namespaces": [
    "urn:parsarium:catalog",
    "urn:parsarium:item"
  ],
  "root": "{urn:parsarium:catalog}catalog",
  "text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ]
}
```

## Run this target

```sh
python3 parsarium.py build xml cpp gsoap
python3 parsarium.py run xml cpp gsoap controls/xml/catalog-ns.xml
```
