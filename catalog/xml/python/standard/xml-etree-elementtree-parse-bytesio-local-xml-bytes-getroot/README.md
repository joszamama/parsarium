# xml.etree.ElementTree.parse(BytesIO(local XML bytes)); getroot() — XML / Python

**Pilot / incomplete format cell.**

- **Runtime:** CPython 3.14.4 ElementTree with Expat 2.10.0
- **Parser family:** See standard API inventory
- **Official documentation:** [reference](https://docs.python.org/3.14/library/xml.etree.elementtree.html)
- **Valid control:** [`controls/xml/two-items.xml`](../../../../../controls/xml/two-items.xml)
- **Inventory:** [standard API record](../../../../../data/python/xml/standard.json) · [saved result](../../../../../projects/xml/python/stdlib_elementtree/verification.json)

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
python3 parsarium.py build xml python stdlib_elementtree
python3 parsarium.py run xml python stdlib_elementtree controls/xml/two-items.xml
```
