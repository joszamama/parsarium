# libxmlb — XML / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.3.30`
- **License:** LGPL-2.1-or-later
- **Parser family:** GLib GMarkup (via libxmlb's XbBuilder)
- **Local input API:** `xb_builder_source_new(); xb_builder_source_load_xml(source, NUL-terminated copy of the local bytes, XB_BUILDER_SOURCE_FLAG_LITERAL_TEXT, &error); xb_builder_new(); xb_builder_import_source; xb_builder_compile(builder, XB_BUILDER_COMPILE_FLAG_NONE, NULL, &error); walk the XbSilo from xb_silo_get_root with xb_node_get_element, xb_node_attr_iter_init/next, xb_node_get_text, xb_node_get_child, xb_node_get_next and xb_node_get_tail`
- **Documentation:** [API reference](<https://github.com/hughsie/libxmlb/blob/0.3.30/src/xb-builder-source.c>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/c/xml/parsers.json) · [control result](../../../../projects/xml/c/libxmlb/verification.json)

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

## Verification scope

Measured as a raw-name XML tree path, not as a namespace-aware parser. Qualified element and attribute names, attribute order and xmlns declarations are compared as strings with expat in non-namespace mode; no namespace URI, expanded name or in-scope binding is produced by libxmlb or GMarkup or inferred by the harness. Comments and processing instructions only end text runs in the oracle; libxmlb does not store them.

## Run this target

```sh
python3 parsarium.py build xml c libxmlb
python3 parsarium.py run xml c libxmlb controls/xml/catalog-ns.xml
```
