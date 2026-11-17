# GO × XML: selected parsers (pilot)

8 control-verified third-party paths selected. The ceiling is ten; selected ranks cover only verified paths from the bounded search. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

pkg.go.dev Imported by package count, from the bounded search captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [github.com/beevik/etree](https://pkg.go.dev/github.com/beevik/etree@v1.8.1) | v1.8.1 | 2,098 | XML 1.0 UTF-8 document into an element tree with namespace lookup | etree element tree over Go encoding/xml Decoder tokenizer |
| 2 | [github.com/antchfx/xmlquery](https://pkg.go.dev/github.com/antchfx/xmlquery@v1.5.2) | v1.5.2 | 627 | XML 1.0 UTF-8 document into an XPath-ready DOM with expanded names | xmlquery DOM over Go encoding/xml Decoder tokenizer |
| 3 | [github.com/clbanning/mxj](https://pkg.go.dev/github.com/clbanning/mxj@v1.8.4) | v1.8.4 | 553 | XML 1.0 UTF-8 document into a map[string]interface{} keyed by local names; namespace URIs, sibling order, comments and PIs are lost | mxj map conversion over Go encoding/xml Decoder tokenizer |
| 4 | [github.com/beego/x2j](https://pkg.go.dev/github.com/beego/x2j@v0.0.0-20131220205130-a0352aadc542) | v0.0.0-20131220205130-a0352aadc542 | 436 | XML 1.0 UTF-8 document into a map[string]interface{} keyed by local names; namespace URIs, sibling order, comments and PIs are lost, and the []byte/string APIs delete whitespace before every '<', including inside CDATA | x2j map conversion over Go encoding/xml Decoder tokenizer |
| 5 | [github.com/vmware/govmomi/vim25/xml](https://pkg.go.dev/github.com/vmware/govmomi/vim25/xml@v0.56.2#NewDecoder) | v0.56.2 | 163 | Full XML 1.0 UTF-8 document into namespace-resolved tokens | separately compiled govmomi fork of Go encoding/xml tokenizer |
| 6 | [github.com/mmcdole/goxpp](https://pkg.go.dev/github.com/mmcdole/goxpp@v1.3.0#NewXMLPullParser) | v1.3.0 | 132 | XML 1.0 UTF-8 document through a pull event cursor with expanded element names, attributes, decoded text and depth | goxpp cursor over Go encoding/xml Decoder tokenizer |
| 7 | [github.com/moovweb/gokogiri/xml](https://pkg.go.dev/github.com/moovweb/gokogiri/xml@v0.0.0-20180713195410-a1a828153468#Parse) | v0.0.0-20180713195410-a1a828153468 | 108 | Local UTF-8 bytes through `xml.Parse`; namespace-aware DOM summary on both valid controls | Go cgo binding over libxml2 2.15.4 XML parser |
| 8 | [github.com/go-forks/go-pkg-xmlx](https://pkg.go.dev/github.com/go-forks/go-pkg-xmlx@v0.0.0-20151201012946-76f54ee73233#Document.LoadBytes) | v0.0.0-20151201012946-76f54ee73233 | 20 | XML 1.0 UTF-8 document loaded into a node tree with expanded names, attributes, namespace declarations, decoded text/CDATA, comment and PI nodes | go-pkg-xmlx node tree over Go encoding/xml Decoder tokenizer |

## Standard API (unranked)

| API | Runtime | Parser family |
| --- | --- | --- |
| [encoding/xml.Decoder.Token()](https://pkg.go.dev/encoding/xml@go1.27.1#Decoder.Token) | Go 1.27.1 | Go encoding/xml Decoder tokenizer |

etree reads through `encoding/xml.Decoder.RawToken`; xmlquery, mxj, x2j and goxpp read through `encoding/xml.Decoder.Token`. Those five third-party paths and the standard API share one runtime tokenizer. govmomi/vim25/xml contains a separately compiled tokenizer fork derived from Go encoding/xml source. etree and xmlquery each build their own trees; mxj and x2j build maps; goxpp maintains a pull cursor with depth and namespace state. mxj's 553 counts only the v1 module path; the v2 path (178) stays a separate lead.

x2j has no tagged release; it is pinned at the only proxy pseudo-version, a GitHub fork of `github.com/clbanning/x2j` frozen in 2013 by the author who later wrote mxj. Its 436 importers count only the beego fork path, likely mostly older beego code; the upstream `github.com/clbanning/x2j` (47) stays a separate lead. Its `Unmarshal`, `ByteDocToMap` and `DocToMap` run the regular expression `[ \t\n\r]*<` over the raw document before tokenizing, so the catalog control's CDATA `x < y` comes back as `x< y`. `ToMap(io.Reader)` skips that step and keeps indentation as `#text` entries. An expat projection onto the map fields ([oracle check](x2j-oracle-check.json)) matches the reader map on both controls and the byte map everywhere except that CDATA value. Its AFL++ bridge maps x2j blocks, and a second probe through the same harness maps encoding/xml blocks; both repeat exactly, but x2j's own blocks differ between the two controls by one block (the nested-map branch at x2j.go:315), against 30 encoding/xml blocks. `encoding/xml` itself shows 79,507 importers but stays outside the third-party ranking.

goxpp uses the documented `NewXMLPullParser(io.Reader, true, nil)` and `NextToken()` API on local byte streams. Its two valid controls match the namespace-aware expected summaries. The catalog control covers 84 goxpp source lines and 306 underlying `encoding/xml` lines. Its own AFL++ blocks repeat identically per control and differ by three between controls, all in comment event handling; a separate `encoding/xml` trace differs by 32 blocks. The 132 importers rank sixth among verified paths. Two higher-adoption leads remain unresolved.

govmomi/vim25/xml exposes the general `NewDecoder(io.Reader).Token()` API. The pinned `v0.56.2` Docker build matches both namespace-aware control summaries and covers 290 lines in its own forked `xml.go`. Parser-only AFL++ traces repeat identically per control and differ by 30 source blocks and 30 tuples; every changed block is in `xml.go`. The source lock pins the 12,553,438-byte whole govmomi module archive. Its 163 Imported by count is for the `vim25/xml` package and ranks fifth among verified paths; it is not an XML-call count.

gokogiri's `xml.Parse([]byte)` cgo route builds a DOM through native libxml2. Both namespace-aware controls match the independently specified summaries. The first covers 93 Go binding lines and 1,730 libxml2 parser lines. The AFL++ target instruments only `parser.c`, `parserInternals.c`, and `entities.c`; full and parse-only maps are identical, so DOM traversal contributes no tuples. Five repeats per control are stable, with 364 tuple IDs differing between the two valid controls. It shares the libxml2 parser family counted in C and C++ and is ranked by its Go package's 108 importers, not by libxml2 adoption.
go-pkg-xmlx's `Document.LoadBytes([]byte, nil)` runs `LoadStream`, which builds its own node tree (element, text, comment, directive and processing-instruction nodes) from `encoding/xml.Decoder.Token`. Both namespace-aware controls match the expat oracle summaries. The catalog control covers 44 package lines (`document.go`, `node.go`) and 294 underlying `encoding/xml` lines. Its own AFL++ blocks repeat per control and differ by two between controls, the comment and processing-instruction node branches; a separate `encoding/xml` trace differs by 30 blocks ([receipt](../../../fuzzing/afl-native/xml/go/github_com_go_forks_go_pkg_xmlx/differential.json)). The module has no tagged release and is pinned at its only proxy pseudo-version. It is a fork of the original jteeuwen/go-pkg-xmlx; `github.com/mattn/go-pkg-xmlx` (15) is byte-identical in all three non-test source files and is not counted.

## Lead log

Numeric leads from the same snapshot, not verified and not selected. Renderers, HTTP clients, Office/OOXML, SAML and xmldsig, JUnit, libvirt, and AWS serializer hits were not treated as parser leads.

| Lead | Version seen | Imported by | Status |
| --- | --- | ---: | --- |
| [github.com/basgys/goxml2json](https://pkg.go.dev/github.com/basgys/goxml2json@v1.1.0#Convert) | v1.1.0 | 182 | [Both valid controls parsed](goxml2json-lead-check.json), but conversion drops namespace URIs from element and attribute names, so the shared namespace-aware result fails. Unselected; Docker coverage and AFL feedback were not run. |
| [github.com/clbanning/mxj/v2](https://pkg.go.dev/github.com/clbanning/mxj/v2) | v2.7.0 | 178 | v2 module of clbanning/mxj; its XML path is expected to follow the verified v1.8.4 map conversion over encoding/xml, but the v2 source was not compared or run. Its 178 importers are not added to the v1 metric. |
| [mellium.im/xmlstream](https://pkg.go.dev/mellium.im/xmlstream) | v0.15.4 | 86 | Excluded after pinned two-valid-control probe: consumes a caller-supplied xml.TokenReader; byte parsing delegates to encoding/xml. Own package supplies no local bytes-to-token parser. |
| [github.com/jbowtie/gokogiri/xml](https://pkg.go.dev/github.com/jbowtie/gokogiri/xml) | v0.0.0-...-de0f9d4 | 71 | cgo binding to libxml2 (gokogiri fork); pseudo-version only, not run. |
| [github.com/clbanning/x2j](https://pkg.go.dev/github.com/clbanning/x2j) | v0.0.0-...-8252494 | 47 | Upstream of the verified github.com/beego/x2j fork, 27 commits ahead of the forked commit a0352aa; its later source was not compared or run. Its 47 importers are not added to the beego/x2j metric. |
| [aqwari.net/xml/xmltree](https://pkg.go.dev/aqwari.net/xml/xmltree) | v0.0.0-...-d9421b2 | 43 | Excluded after pinned two-valid-control probe: tree built from `encoding/xml` tokens; matches an expat oracle, but xmltree-scoped AFL++ feedback is identical on the fixed control pair (all 30 differences in `encoding/xml`). [Evidence](xmltree-lead-check.json). |
| [github.com/nbio/xml](https://pkg.go.dev/github.com/nbio/xml) | v0.0.0-...-9f64bb3 | 35 | Synopsis is identical to encoding/xml, which suggests a fork in the encoding/xml family. Not checked or run. |
| [github.com/lestrrat-go/libxml2](https://pkg.go.dev/github.com/lestrrat-go/libxml2) | v0.0.0-...-3f0f7bd | 30 | cgo interface to libxml2; pseudo-version only, native build not attempted. |
| [github.com/tdewolff/parse/v2/xml](https://pkg.go.dev/github.com/tdewolff/parse/v2/xml) | v2.25.0 | 28 | XML 1.0 lexer (tokenizer, not a tree or namespace resolver); not run. |

Queries: `xml`, `xml parser`, `xml decoder`, `xml dom`, `xml tree`, `xml reader`; limit 100 each; 496 hits, 464 unique.
