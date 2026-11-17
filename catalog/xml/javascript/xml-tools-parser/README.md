# @xml-tools/parser — JavaScript XML CST

- **Release:** `@xml-tools/parser` 1.0.12, Apache-2.0; [pinned npm tarball](https://registry.npmjs.org/@xml-tools/parser/-/parser-1.0.12.tgz) and [source lock](../../../../projects/xml/javascript/xml_tools_parser/source-lock.json)
- **Adoption:** 7,478,313 npm downloads in the saved 30-day JavaScript XML window; this measures package downloads, including transitive use
- **Local API:** [`parse(text)`](https://unpkg.com/@xml-tools/parser@1.0.12/README.md) after strict UTF-8 decoding of local bytes
- **Parser family:** XML grammar and lexer from this package over the Chevrotain 7.1.1 CST engine. It is distinct from the selected sax-js, saxes, and xmldom XML grammars.
- **Runnable target:** [Docker harness, both control outputs, coverage, and AFL++ feedback](../../../../projects/xml/javascript/xml_tools_parser/README.md)

The observed result is a nested XML concrete syntax tree with raw element QNames, ordered attribute QNames and raw quoted values. `c:catalog`, `p:amount`, and the `xmlns` attributes remain token images; `&quot;` is not decoded. Both valid controls have no lexer or parser errors, and their raw name hierarchy matches independent Expat parsing without namespace expansion. This is a **raw XML grammar path**, not a claim of resolved namespace URIs or decoded text. The package's own README describes fault-tolerant error recovery, so partial CST behavior outside these valid controls remains untested.
