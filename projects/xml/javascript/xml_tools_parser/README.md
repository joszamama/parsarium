# @xml-tools/parser — XML / JavaScript

Pinned release: `1.0.12`. [Manifest](manifest.json) · [Docker control receipt](verification.json) · [AFL++ feedback receipt](../../../../data/javascript/xml/xml-tools-parser-feedback.json)

This target passes strictly decoded local UTF-8 text to the package's documented `parse(text)` API. Its result is a **raw concrete syntax tree projection**: nested element QNames, ordered attribute QNames with original quoted token images, maximum depth, token count, and lexer/parser error counts. The package does not resolve namespace URIs or decode entity references in this CST. The adapter leaves `c:catalog`, `xmlns:c`, and `&quot;` as returned, so this target does not claim XML Namespaces or decoded text semantics.

## Run from the repository root

```sh
python3 parsarium.py build xml javascript xml_tools_parser
python3 parsarium.py run xml javascript xml_tools_parser controls/xml/catalog-ns.xml
python3 parsarium.py run xml javascript xml_tools_parser controls/xml/order-default-ns.xml
python3 parsarium.py afl build xml javascript xml_tools_parser
python3 parsarium.py afl prepare xml javascript xml_tools_parser runs/xml-xml_tools_parser-afl
python3 projects/xml/javascript/xml_tools_parser/verify_feedback.py
```

The fixed controls contain namespace prefixes and declarations. [`oracle.py`](oracle.py) uses independent Python Expat parsing **without namespace expansion** to verify the element and attribute QName hierarchy. The control result checks the package's lexical values separately against the pinned expected output. Both controls have zero lexer and parser errors.

V8 coverage counts 351 lines in the package's XML grammar and lexer and 5,225 lines in the underlying Chevrotain 7.1.1 parser engine. AFL++ feedback uses only hit counts for `ALT` grammar callbacks in the package's `lib/parser.js`. Three fresh runs of each valid control were stable. The two controls differ by 22 package callback-count features and 22 AFL tuples, although both have 17 features and 37 tuples each. A no-parse baseline imports the harness and reads/decodes each control; its 17 constructor self-analysis features are identical for both files. Eleven callback hit counts change only after the package parse is invoked. This is execution-frequency guidance, not newly discovered branches or lines. No campaign or malformed-input test was run.

The parser is fault tolerant and can return partial CSTs on invalid text. These two valid controls do not establish broader XML conformance.
