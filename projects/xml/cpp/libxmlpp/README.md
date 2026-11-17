# libxml++ — XML / C++

Pinned release: `5.6.1` (LGPL-2.1-or-later), with its underlying libxml2 parser pinned to `2.15.4` (MIT). [Manifest](manifest.json) · [source lock](source-lock.json) · [verification receipt](verification.json)

`xmlpp::DomParser::parse_memory_raw(const unsigned char*, size_type)` parses local XML bytes into a namespace-aware DOM. libxml++ wraps the libxml2 C parser, so this package is a separate C++ API but belongs to the libxml2 parser family. Its primary adoption measure is 275 Debian `-dev` package installations summed across three ABI packages, rank 4 of the four searched C++ XML packages; only seven of those installations are for the ABI-5 development package matching this release family. [Cell ranking](../../../../data/cpp/xml/ranking.md)

The two valid controls cover prefixed and default namespaces, namespace resets, attributes, entity references, CDATA, UTF-8 text, a comment, and a processing instruction. Their exact outputs are pinned in [the manifest](manifest.json). The container checks the first control, records LLVM source coverage in libxml++ and libxml2 `parser.c`, and exposes `/work/replay` for local files. [The parser-only feedback probe](parser-probe.cpp) calls `parse_memory_raw` without DOM traversal. Its AFL++ maps repeat exactly and differ between controls. A few `parser.c` line hits vary between identical runs, so its reported line difference uses only lines stable within each control. [Feedback receipt](../../../../fuzzing/afl-native/xml/cpp/libxmlpp/differential.json)

## Run from the repository root

```sh
python3 parsarium.py build xml cpp libxmlpp
python3 parsarium.py run xml cpp libxmlpp controls/xml/catalog-ns.xml
python3 parsarium.py run xml cpp libxmlpp controls/xml/order-default-ns.xml
python3 parsarium.py replay xml cpp libxmlpp CORPUS_DIR runs/xml-libxmlpp-replay
python3 parsarium.py afl build xml cpp libxmlpp
python3 parsarium.py afl prepare xml cpp libxmlpp runs/xml-libxmlpp-afl
python3 projects/xml/cpp/libxmlpp/verify-feedback.py
```

`CORPUS_DIR` is a directory of XML files to replay. The AFL++ command prepares a run; it does not start a campaign. The controls establish the stated XML 1.0 UTF-8 scope, not full DTD, encoding, or malformed-input behavior.
