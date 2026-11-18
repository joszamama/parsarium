# libucw-xml — XML / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `6.5`
- **License:** LGPL-2.0-or-later
- **Parser family:** LibUCW ucw-xml
- **Local input API:** `xml_init(&ctx); ctx.h_warn = ctx.h_error = ctx.h_fatal = (failure recorder); ctx.flags |= XML_ALLOC_ALL; xml_ns_enable(&ctx); fbbuf_init_read(fastbuf, copy of the local bytes, size, 0); xml_push_fastbuf(&ctx, fastbuf); ctx.pull = XML_PULL_CHARS | XML_PULL_STAG | XML_PULL_ETAG | XML_PULL_COMMENT | XML_PULL_PI; xml_next(&ctx) until 0 (XML_STATE_STAG: ctx.node ns/name and XML_ATTR_FOR_EACH ns/name/val, xml_ns_by_id; XML_STATE_CHARS: ctx.node text/len; XML_STATE_ETAG/COMMENT/PI); ctx.err_code; xml_cleanup(&ctx)`
- **Documentation:** [API reference](<https://www.ucw.cz/libucw/doc/ucw-xml/>)
- **Valid control:** [`controls/xml/catalog-ns.xml`](../../../../controls/xml/catalog-ns.xml)
- **Catalog evidence:** [parser record](../../../../data/c/xml/parsers.json) · [control result](../../../../projects/xml/c/libucw_xml/verification.json)

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

## Verification scope

Namespace-aware path: both valid controls give the exact shared summary, including declaration counts 2 and 3.

## Run this target

```sh
python3 parsarium.py build xml c libucw_xml
python3 parsarium.py run xml c libucw_xml controls/xml/catalog-ns.xml
```
