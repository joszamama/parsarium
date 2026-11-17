# XML / Go — pilot

**Status:** pilot_four_selected_search_bounded; incomplete. 4 verified third-party paths, 1 verified standard APIs, 4 verified Docker harnesses.

Pilot cell: the four highest Imported-by XML parser leads (etree 2,098; xmlquery 627; mxj 553; beego/x2j 436) were built and control-verified. All four use the Go encoding/xml Decoder tokenizer and build their own trees or maps; none is an independent tokenizer. mxj's map drops namespace URIs and prefixes, order between differently named siblings, comments, processing instructions and mixed-content runs, so only its map paths, attribute keys and trimmed text are claimed. beego/x2j has the same map losses; in addition its []byte/string APIs delete whitespace before every '<' in the raw document, which changes CDATA content on the valid catalog control ('x < y' becomes 'x< y'), and its io.Reader API keeps indentation as '#text' entries. x2j is pinned at its only pseudo-version (a 2013 fork of clbanning/x2j); its own AFL++ blocks differ between the two controls by only one block, while its encoding/xml blocks differ by 30. 12 further numeric leads remain unresolved and are not selected or ranked. The first 100 hits of six queries were captured (xml dom returned 68; xml reader 28). The two small valid UTF-8 XML 1.0 controls without DOCTYPE do not establish DTD, entity declaration, non-UTF-8 encoding, XML 1.1, or attribute-value normalization behaviour.

[Ranking and search limits](../../../data/go/xml/ranking.md) · [Standard API inventory](../../../data/go/xml/standard.json)

## Third-party parsers

- [github.com/beevik/etree](github-com-beevik-etree/README.md) — verified Docker harness
- [github.com/antchfx/xmlquery](github-com-antchfx-xmlquery/README.md) — verified Docker harness
- [github.com/clbanning/mxj](github-com-clbanning-mxj/README.md) — verified Docker harness
- [github.com/beego/x2j](github-com-beego-x2j/README.md) — verified Docker harness

## Standard and runtime APIs

- [encoding/xml.Decoder.Token()](standard/encoding-xml-decoder-token/README.md) — verified Docker harness
