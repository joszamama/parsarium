# XML / Go — pilot

**Status:** pilot_ten_selected_search_bounded; incomplete. 10 verified third-party paths, 1 verified standard APIs, 10 verified Docker harnesses.

Ten Go XML package paths pass two valid namespace-aware controls with parser-source coverage and stable AFL++ feedback, in pkg.go.dev Imported by order from the 2026-11-17 snapshot: etree 2,098; xmlquery 627; mxj 553; beego/x2j 436; govmomi/vim25/xml 163; goxpp 132; gokogiri/xml 108; lestrrat-go/libxml2 30; go-pkg-xmlx 20; helium 12. Ranks cover selected verified paths only. Families: six paths (etree, xmlquery, mxj, x2j, goxpp, go-pkg-xmlx) are package-specific tree, map, cursor or node APIs over the Go encoding/xml runtime tokenizer; govmomi/vim25/xml is a separately compiled encoding/xml fork; gokogiri and lestrrat-go/libxml2 are two cgo bindings over the same pinned libxml2 2.15.4 build, whose AFL++ feedback is restricted to libxml2 parser sources (shared-parser feedback; lestrrat-go/libxml2 needs a one-line cgo type patch for libxml2 2.15 headers and its repository is archived); helium is an independent pure-Go parser with no encoding/xml or cgo. Each encoding/xml wrapper's own AFL++ blocks differ between the fixed valid controls (go-pkg-xmlx by two, in comment and PI nodes), measured separately from encoding/xml. mxj and x2j map routes lose namespace URIs/prefixes and mixed-content details; x2j byte/string routes alter CDATA whitespace on the valid catalog control, while its selected reader route preserves it. Higher-adoption leads were excluded with evidence rather than skipped: goxml2json (182) because its own XML decoder covers identical blocks on both controls (its only differing blocks are JSON-encoder code) and it keeps only local names; mxj/v2 (178, 86.6% source overlap with selected mxj), jbowtie/gokogiri (95.8% with moovweb/gokogiri), clbanning/x2j (72.5%; x2j.go 97%), nbio/xml (90.2% with the selected govmomi fork) and three other encoding/xml forks (85-95%), mattn/go-pkg-xmlx (byte-identical), a vendored etree copy (97.9% with etree v1.0.1) and xquery (deprecated predecessor of xmlquery) as same-parser paths; simplexml/dom and go-xmldom by the xmltree own-source feedback gate; xml2map and quickxml because the catalog control fails; tdewolff/parse xml as a lexer without reference decoding; gxml as a wrapper over mxj/v2; validators, minifiers and formatters as non-parsers. helium's 12 ties with three excluded leads, so the tie does not decide the tenth slot. Five lower leads (11 and below) were not evaluated after the ceiling was reached. Six pkg.go.dev queries recorded 496 hits, 464 unique; the first 100 hits per query were captured where available. Two small valid UTF-8 XML 1.0 controls without DOCTYPE do not establish DTD, entity declaration, non-UTF-8 encoding, XML 1.1, or attribute-value normalization behaviour.

[Ranking and search limits](../../../data/go/xml/ranking.md) · [Standard API inventory](../../../data/go/xml/standard.json)

## Third-party parsers

- [github.com/beevik/etree](github-com-beevik-etree/README.md) — verified Docker harness
- [github.com/antchfx/xmlquery](github-com-antchfx-xmlquery/README.md) — verified Docker harness
- [github.com/clbanning/mxj](github-com-clbanning-mxj/README.md) — verified Docker harness
- [github.com/beego/x2j](github-com-beego-x2j/README.md) — verified Docker harness
- [github.com/vmware/govmomi/vim25/xml](github-com-vmware-govmomi-vim25-xml/README.md) — verified Docker harness
- [github.com/mmcdole/goxpp](github-com-mmcdole-goxpp/README.md) — verified Docker harness
- [github.com/moovweb/gokogiri/xml](github-com-moovweb-gokogiri-xml/README.md) — verified Docker harness
- [github.com/lestrrat-go/libxml2](github-com-lestrrat-go-libxml2/README.md) — verified Docker harness
- [github.com/go-forks/go-pkg-xmlx](github-com-go-forks-go-pkg-xmlx/README.md) — verified Docker harness
- [github.com/lestrrat-go/helium](github-com-lestrrat-go-helium/README.md) — verified Docker harness

## Standard and runtime APIs

- [encoding/xml.Decoder.Token()](standard/encoding-xml-decoder-token/README.md) — verified Docker harness
