# jackson-dataformat-xml — XML / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.23.0`
- **Upstream:** [source repository](<https://github.com/FasterXML/jackson-dataformat-xml>) · [Maven Central](<https://central.sonatype.com/artifact/com.fasterxml.jackson.dataformat/jackson-dataformat-xml>)
- **License:** Apache-2.0
- **Parser family:** Jackson XML FromXmlParser/XmlTokenStream over Woodstox StAX tokenizer
- **Local input API:** `new XmlFactory(new WstxInputFactory()).createParser(Files.newInputStream(local Path)); nextToken() to EOF`
- **Documentation:** [API reference](<https://github.com/FasterXML/jackson-dataformat-xml>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/java/xml/parsers.json) · [control result](../../../../data/java/xml/verification.json)

## Observed control result

```json
{
  "events": [
    "START_OBJECT",
    "FIELD_NAME:version",
    "VALUE_STRING:1",
    "FIELD_NAME:item",
    "START_OBJECT",
    "FIELD_NAME:id",
    "VALUE_STRING:a1",
    "FIELD_NAME:lang",
    "VALUE_STRING:es",
    "FIELD_NAME:",
    "VALUE_STRING:Café & té",
    "END_OBJECT",
    "FIELD_NAME:item",
    "START_OBJECT",
    "FIELD_NAME:id",
    "VALUE_STRING:b2",
    "FIELD_NAME:name",
    "VALUE_STRING:Zürich <HQ>",
    "FIELD_NAME:note",
    "VALUE_STRING:x < y",
    "END_OBJECT",
    "END_OBJECT"
  ],
  "token_count": 22
}
```

## Run this target

```sh
python3 parsarium.py build xml java jackson_xml
python3 parsarium.py run xml java jackson_xml controls/xml/catalog-ns.xml
```
