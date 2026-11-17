# XML / Go — pilot

**Status:** pilot_five_selected_search_bounded; incomplete. 5 verified third-party paths, 1 verified standard APIs, 5 verified Docker harnesses.

Five Go XML package paths pass two valid namespace-aware controls with parser and underlying source coverage plus stable AFL++ feedback: etree 2,098; xmlquery 627; mxj 553; beego/x2j 436; goxpp 132 Imported by. All five use Go encoding/xml Decoder as their tokenizer. goxpp builds a pull cursor with its own depth/namespace state; its valid controls differ by three own-source AFL++ blocks, all in comment event handling, and 32 encoding/xml blocks, with stable repeats. Higher-adoption goxml2json (182), mxj/v2 (178), and govmomi XML (163), plus eight other numeric leads, remain unverified; ranks cover selected verified paths only. mxj and x2j map routes lose namespace URIs/prefixes and mixed-content details; x2j byte/string routes also alter CDATA whitespace on the valid catalog control, while its selected reader route preserves it. Six pkg.go.dev queries recorded 496 hits, 464 unique; the first 100 hits per query were captured where available. Two small valid UTF-8 XML 1.0 controls without DOCTYPE do not establish DTD, entity declaration, non-UTF-8 encoding, XML 1.1, or attribute-value normalization behaviour.

[Ranking and search limits](../../../data/go/xml/ranking.md) · [Standard API inventory](../../../data/go/xml/standard.json)

## Third-party parsers

- [github.com/beevik/etree](github-com-beevik-etree/README.md) — verified Docker harness
- [github.com/antchfx/xmlquery](github-com-antchfx-xmlquery/README.md) — verified Docker harness
- [github.com/clbanning/mxj](github-com-clbanning-mxj/README.md) — verified Docker harness
- [github.com/beego/x2j](github-com-beego-x2j/README.md) — verified Docker harness
- [github.com/mmcdole/goxpp](github-com-mmcdole-goxpp/README.md) — verified Docker harness

## Standard and runtime APIs

- [encoding/xml.Decoder.Token()](standard/encoding-xml-decoder-token/README.md) — verified Docker harness
