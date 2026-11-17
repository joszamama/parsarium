# libxml++ — XML / C++

- **Pinned release:** `5.6.1` (LGPL-2.1-or-later)
- **Underlying parser:** libxml2 `2.15.4` (MIT); shared libxml2 parser family
- **Local input API:** `xmlpp::DomParser::parse_memory_raw(const unsigned char*, size_type)` ([pinned header](https://github.com/libxmlplusplus/libxmlplusplus/blob/5.6.1/libxml%2B%2B/parsers/domparser.h))
- **Valid controls:** [namespace catalog](../../../../controls/xml/catalog-ns.xml) and [namespace order](../../../../controls/xml/order-default-ns.xml)
- **Adoption:** rank 4 of the four searched C++ XML libraries by Debian development package installations, 275 across three libxml++ ABI packages; the ABI-5 package has seven. [Ranking and limits](../../../../data/cpp/xml/ranking.md)
- **Evidence:** [parser record](../../../../data/cpp/xml/parsers.json), [exact control results](../../../../data/cpp/xml/verification.json), [parser-only AFL++ feedback](../../../../fuzzing/afl-native/xml/cpp/libxmlpp/differential.json)

The controls produce namespace-expanded element and attribute names, text, depth, and namespace declarations. The [runnable project](../../../../projects/xml/cpp/libxmlpp/README.md) contains the Docker build, byte-buffer harness, and source-coverage checks.
