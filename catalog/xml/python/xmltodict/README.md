# xmltodict — XML / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.0.4`
- **Upstream:** [source repository](<https://github.com/martinblech/xmltodict>) · [PyPI](<https://pypi.org/project/xmltodict/>)
- **License:** MIT
- **Parser family:** xmltodict over CPython pyexpat / Expat
- **Local input API:** `xmltodict.parse(BytesIO(local UTF-8 XML bytes), process_namespaces=True, disable_entities=True)`
- **Documentation:** [API reference](<https://pypi.org/project/xmltodict/>)
- **Valid control:** [`controls/xml/two-items.xml`](../../../../controls/xml/two-items.xml)
- **Catalog evidence:** [parser record](../../../../data/python/xml/parsers.json) · [control result](../../../../data/python/xml/verification.json)

## Observed control result

```json
{
  "root": "library",
  "namespace": "urn:parsarium:xml:pilot",
  "child_count": 2,
  "first_item_id": "7",
  "first_item_text": "A & B",
  "second_item_text": "π"
}
```

## Run this target

```sh
python3 parsarium.py build xml python xmltodict
python3 parsarium.py run xml python xmltodict controls/xml/two-items.xml
```
