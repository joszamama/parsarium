# xml-js — XML / JavaScript

Pinned `xml-js` 1.6.11 with a strict UTF-8 local-byte adapter, a Dockerized control replay, V8 source coverage, and a parser-scoped AFL++ bridge. The parser family is the same pinned `sax` 1.6.1 tokenizer used by the selected `sax` and `xml2js` paths.

[Manifest](manifest.json) · [source lock](source-lock.json) · [control receipt](verification.json) · [API, result, and scope](../../../../catalog/xml/javascript/xml_js/README.md)

Run from the repository root:

```sh
python3 parsarium.py build xml javascript xml_js
python3 parsarium.py run xml javascript xml_js controls/xml/catalog-ns.xml
python3 parsarium.py run xml javascript xml_js controls/xml/order-default-ns.xml
python3 parsarium.py afl build xml javascript xml_js
python3 parsarium.py afl prepare xml javascript xml_js runs/xml-xml-js-afl
```
