# GO × XML: selected parsers (pilot)

1 control-verified third-party path selected. The ceiling is ten; this pilot builds only the highest-adoption XML parser lead and does not pad the selection. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

pkg.go.dev Imported by package count, from the bounded search captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [github.com/beevik/etree](https://pkg.go.dev/github.com/beevik/etree@v1.8.1) | v1.8.1 | 2,098 | XML 1.0 UTF-8 document into an element tree with namespace lookup | etree element tree over Go encoding/xml Decoder tokenizer |

## Standard API (unranked)

| API | Runtime | Parser family |
| --- | --- | --- |
| [encoding/xml.Decoder.Token()](https://pkg.go.dev/encoding/xml@go1.27.1#Decoder.Token) | Go 1.27.1 | Go encoding/xml Decoder tokenizer |

etree reads through `encoding/xml.Decoder.RawToken`, so both rows share the Go encoding/xml tokenizer. Only etree's tree building and namespace lookup are separate code. `encoding/xml` itself shows 79,507 importers but stays outside the third-party ranking.

## Lead log

Numeric leads from the same snapshot, not verified and not selected. Renderers, HTTP clients, Office/OOXML, SAML and xmldsig, JUnit, libvirt, and AWS serializer hits were not treated as parser leads.

| Lead | Version seen | Imported by | Status |
| --- | --- | ---: | --- |
| [github.com/antchfx/xmlquery](https://pkg.go.dev/github.com/antchfx/xmlquery) | v1.5.2 | 627 | XPath query DOM documented as xmlquery.Parse(io.Reader); its tokenizer and namespace handling were not checked and no control was run. |
| [github.com/clbanning/mxj](https://pkg.go.dev/github.com/clbanning/mxj) | v1.8.4 | 553 | Converts XML to map[string]interface{} via NewMapXml([]byte); not run. A v2 module path is logged separately. |
| [github.com/beego/x2j](https://pkg.go.dev/github.com/beego/x2j) | v0.0.0-...-a0352aa | 436 | Unmarshals arbitrary XML to map values; pseudo-version only, not run. |
| [github.com/basgys/goxml2json](https://pkg.go.dev/github.com/basgys/goxml2json) | v1.1.0 | 182 | XML-to-JSON converter over an io.Reader; not run. |
| [github.com/clbanning/mxj/v2](https://pkg.go.dev/github.com/clbanning/mxj/v2) | v2.7.0 | 178 | v2 module of clbanning/mxj; would share its decoding path. Not run. |
| [github.com/vmware/govmomi/vim25/xml](https://pkg.go.dev/github.com/vmware/govmomi/vim25/xml) | v0.56.2 | 163 | Synopsis is identical to encoding/xml, which suggests a vendored fork in the encoding/xml family. Not checked or run. |
| [github.com/mmcdole/goxpp](https://pkg.go.dev/github.com/mmcdole/goxpp) | v1.3.0 | 132 | XML pull parser API; its tokenizer source was not checked and no control was run. |
| [github.com/moovweb/gokogiri/xml](https://pkg.go.dev/github.com/moovweb/gokogiri/xml) | v0.0.0-...-a1a8281 | 108 | cgo binding to libxml2; pseudo-version only, native build not attempted. |
| [mellium.im/xmlstream](https://pkg.go.dev/mellium.im/xmlstream) | v0.15.4 | 86 | Streaming token transformer API; whether it is a parser or a token-stream utility was not settled. Not run. |
| [github.com/jbowtie/gokogiri/xml](https://pkg.go.dev/github.com/jbowtie/gokogiri/xml) | v0.0.0-...-de0f9d4 | 71 | cgo binding to libxml2 (gokogiri fork); pseudo-version only, not run. |
| [github.com/clbanning/x2j](https://pkg.go.dev/github.com/clbanning/x2j) | v0.0.0-...-8252494 | 47 | Unmarshals arbitrary XML to map values; pseudo-version only, not run. |
| [aqwari.net/xml/xmltree](https://pkg.go.dev/aqwari.net/xml/xmltree) | v0.0.0-...-d9421b2 | 43 | Converts XML documents into a tree of Go values; pseudo-version only, not run. |
| [github.com/nbio/xml](https://pkg.go.dev/github.com/nbio/xml) | v0.0.0-...-9f64bb3 | 35 | Synopsis is identical to encoding/xml, which suggests a fork in the encoding/xml family. Not checked or run. |
| [github.com/lestrrat-go/libxml2](https://pkg.go.dev/github.com/lestrrat-go/libxml2) | v0.0.0-...-3f0f7bd | 30 | cgo interface to libxml2; pseudo-version only, native build not attempted. |
| [github.com/tdewolff/parse/v2/xml](https://pkg.go.dev/github.com/tdewolff/parse/v2/xml) | v2.25.0 | 28 | XML 1.0 lexer (tokenizer, not a tree or namespace resolver); not run. |

Queries: `xml`, `xml parser`, `xml decoder`, `xml dom`, `xml tree`, `xml reader`; limit 100 each; 496 hits, 464 unique.
