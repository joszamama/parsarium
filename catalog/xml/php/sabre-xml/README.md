# sabre/xml — XML / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `4.1.0`
- **Upstream:** [source repository](<https://github.com/sabre-io/xml>) · [Packagist](<https://packagist.org/packages/sabre/xml>)
- **License:** BSD-3-Clause
- **Parser family:** libxml2 via PHP XMLReader, shared with the standard XMLReader API
- **Local input API:** `Sabre\Xml\Service::getReader() then Sabre\Xml\Reader::XML(string) and Reader::parse(): builds a Clark-notation {namespace}local element tree with attributes and leaf text (Service::parse also accepts a string or stream resource)`
- **Documentation:** [API reference](<https://sabre.io/xml/reading/>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/php/xml/parsers.json) · [control result](../../../../data/php/xml/verification.json)

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
python3 parsarium.py build xml php sabre_xml
python3 parsarium.py run xml php sabre_xml controls/xml/catalog-ns.xml
```
