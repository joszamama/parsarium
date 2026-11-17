# instant-xml — XML / Rust

Pinned release: `0.7.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/rust/instant-xml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml rust instant_xml
python3 parsarium.py run xml rust instant_xml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml rust instant_xml CORPUS_DIR runs/xml-instant_xml-replay
python3 parsarium.py afl build xml rust instant_xml
python3 parsarium.py afl prepare xml rust instant_xml runs/xml-instant_xml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Typed-mapping library over the selected xmlparser tokenizer; its documented generic AnyElement view is the observed result. instant-xml resolves namespaces, decodes references and builds AnyElement itself. It consumes xmlns declarations without exposing them, so the summary has no namespace_declarations count and namespaces lists the URIs of expanded names. AnyElement keeps one text value per element (the last text node), so mixed content is not fully reported. It rejects a processing instruction inside the root element, so the second control is order-default-ns-no-pi.xml.
