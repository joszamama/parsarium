# opensp — XML / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.5.2`
- **Upstream:** [Debian](<https://tracker.debian.org/pkg/opensp>)
- **License:** MIT
- **Parser family:** OpenSP (James Clark's SP) own SGML/XML parser
- **Local input API:** `ParserEventGeneratorKit with addCatalog=pubtext/xml.soc (SGMLDECL xml.dcl) and enableWarning 'xml' and 'no-valid', SP_CHARSET_FIXED=YES and SP_ENCODING=XML as doc/xml.htm documents; makeEventGenerator over the local bytes written to a private temporary file, then EventGenerator::run(SGMLApplication&) with startElement (gi, specified attributes and CDATA chunks), endElement, data, pi and error callbacks`
- **Documentation:** [API reference](<https://openjade.sourceforge.net/doc/generic.htm>)
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
python3 parsarium.py build xml cpp opensp
python3 parsarium.py run xml cpp opensp controls/xml/catalog-ns.xml
```
