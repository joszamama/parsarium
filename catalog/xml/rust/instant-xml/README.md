# instant-xml — XML / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.7.7`
- **License:** Apache-2.0 OR MIT
- **Parser family:** xmlparser (shared with the selected xmlparser path): xmlparser Tokenizer tokenizes; instant-xml adds its own namespace resolver, reference decoder and AnyElement tree builder. Not an independent tokenizer.
- **Local input API:** `instant_xml::from_str::<AnyElement>(&str) -> Result<AnyElement, Error>; AnyElement { ns, name, attributes: Vec<AnyAttribute { ns, name, value }>, text: Option<Cow<str>>, children: Vec<AnyElement> }`
- **Documentation:** [API reference](<https://docs.rs/instant-xml/0.7.7/instant_xml/struct.AnyElement.html>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/rust/xml/parsers.json) · [control result](../../../../projects/xml/rust/instant_xml/verification.json)

## Observed control result

```json
{
  "root": "{urn:parsarium:catalog}catalog",
  "elements": [
    "{urn:parsarium:catalog}catalog",
    "{urn:parsarium:item}item",
    "{urn:parsarium:item}item",
    "{urn:parsarium:item}name",
    "{urn:parsarium:item}note"
  ],
  "max_depth": 3,
  "namespaces": [
    "urn:parsarium:catalog",
    "urn:parsarium:item"
  ],
  "attributes": [
    "version=1",
    "id=a1",
    "{urn:parsarium:catalog}lang=es",
    "id=b2"
  ],
  "text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ]
}
```

## Run this target

```sh
python3 parsarium.py build xml rust instant_xml
python3 parsarium.py run xml rust instant_xml controls/xml/catalog-ns.xml
```
