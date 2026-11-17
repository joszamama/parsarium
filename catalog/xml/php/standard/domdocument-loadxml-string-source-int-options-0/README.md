# DOMDocument::loadXML(string $source, int $options = 0) — XML / PHP

**Pilot / incomplete format cell.**

- **Runtime:** PHP 8.5.12 CLI (source build, --disable-all --with-libxml --enable-dom) with source-built libxml2 2.15.4
- **Parser family:** libxml2 (via PHP ext/libxml)
- **Official documentation:** [reference](https://www.php.net/manual/en/domdocument.loadxml.php)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../../controls/xml/catalog-ns.xml)
- **Inventory:** [standard API record](../../../../../data/php/xml/standard.json) · [saved result](../../../../../projects/xml/php/stdlib_domdocument/verification.json)

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
python3 parsarium.py build xml php stdlib_domdocument
python3 parsarium.py run xml php stdlib_domdocument controls/xml/catalog-ns.xml
```
