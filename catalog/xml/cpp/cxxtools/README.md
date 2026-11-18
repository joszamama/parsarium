# cxxtools — XML / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.0.0`
- **Upstream:** [source repository](<https://github.com/maekitalo/cxxtools>) · [Debian](<https://tracker.debian.org/pkg/cxxtools>)
- **License:** LGPL-2.1-or-later
- **Parser family:** cxxtools XmlReader own state-machine parser
- **Local input API:** `cxxtools::xml::XmlReader(std::istream&) over a std::istringstream of the local bytes; XmlReader::get() then next() until Node::EndDocument; StartElement::name() and attributes() (Attribute::name()/value()), Characters::content(); cxxtools::String converted with Utf8Codec::encode`
- **Documentation:** [API reference](<https://github.com/maekitalo/cxxtools/blob/V3.0/include/cxxtools/xml/xmlreader.h>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/cpp/xml/parsers.json) · [control result](../../../../data/cpp/xml/verification.json)

## Observed control result

```json
{
  "attributes": [
    "xmlns:c=urn:parsarium:catalog",
    "xmlns=urn:parsarium:item",
    "version=1",
    "id=a1",
    "c:lang=es",
    "id=b2"
  ],
  "elements": [
    "c:catalog",
    "item",
    "item",
    "name",
    "note"
  ],
  "max_depth": 3,
  "root": "c:catalog",
  "text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ]
}
```

## Run this target

```sh
python3 parsarium.py build xml cpp cxxtools
python3 parsarium.py run xml cpp cxxtools controls/xml/catalog-ns.xml
```
