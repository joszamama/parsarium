# veewee/xml — XML / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `4.14.0`
- **License:** MIT
- **Parser family:** libxml2 via PHP Dom\XMLDocument, shared with the standard path, sabre/xml, symfony/dom-crawler and symfony/serializer
- **Local input API:** `VeeWee\Xml\Encoding\xml_decode(string $xml, callable ...$configurators): array, documented as "Decodes an XML string into an array". It loads the text with Dom\XMLDocument::createFromString($xml, 0) inside disallow_issues (any libxml error or warning throws, wrapped as EncodingException) and converts the document element into veewee's PHP array format. The same loader backs Dom\Document::fromXmlString; Dom\Document::fromXmlFile and Reader::fromXmlFile/fromXmlString (XMLReader) are the documented file and streaming entry points`
- **Documentation:** [API reference](<https://github.com/veewee/xml/blob/6345edd4afdfa188960663fe849bfe568571c84f/docs/encoding.md#xml_decode>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/php/xml/parsers.json) · [control result](../../../../data/php/xml/verification.json)

## Observed control result

```json
{
  "attributes": [
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
  "namespace_declarations": [
    "0 c:catalog xmlns:c=urn:parsarium:catalog",
    "0 c:catalog xmlns=urn:parsarium:item"
  ],
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
python3 parsarium.py build xml php veewee_xml
python3 parsarium.py run xml php veewee_xml controls/xml/catalog-ns.xml
```
