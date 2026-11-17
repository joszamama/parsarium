# symfony/serializer — XML / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v8.1.11`
- **License:** MIT
- **Parser family:** libxml2 via PHP DOMDocument, shared with the standard path, sabre/xml and symfony/dom-crawler
- **Local input API:** `new XmlEncoder() then XmlEncoder::decode(string $data, 'xml') (DecoderInterface; Serializer::decode delegates to it). With the default context it calls DOMDocument::loadXML with LIBXML_NONET | LIBXML_NOBLANKS, rejects any libxml error or a DOCTYPE, skips comments and processing instructions, and returns the root element's content as a PHP array`
- **Documentation:** [API reference](<https://symfony.com/doc/current/serializer/encoders.html#the-xmlencoder>)
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
    "item",
    "item",
    "name",
    "note"
  ],
  "max_depth": 3,
  "root_namespaces": {
    "": "urn:parsarium:item",
    "c": "urn:parsarium:catalog"
  },
  "text": [
    "Café & té",
    "Zürich <HQ>",
    "x < y"
  ]
}
```

## Run this target

```sh
python3 parsarium.py build xml php symfony_serializer
python3 parsarium.py run xml php symfony_serializer controls/xml/catalog-ns.xml
```
