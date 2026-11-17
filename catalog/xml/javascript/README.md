# XML / JavaScript — pilot

**Status:** pilot_nine_selected_search_bounded; incomplete. 9 verified third-party paths, 0 verified standard APIs, 9 verified Docker harnesses.

Pilot cell with nine verified third-party paths: saxes 6.0.0, jsdom 31.0.1, sax 1.6.1, fast-xml-parser 5.12.1, @xmldom/xmldom 0.9.12, xml2js 0.6.2, xml-js 1.6.11, htmlparser2 12.0.0 xmlMode, and xmldoc 3.0.0 are control-verified, source-covered, and have input-dependent AFL++ feedback. Comparable 30-day npm downloads rank the nine package paths; counts include transitive adoption. The nine paths cover five independent parser families: jsdom shares saxes and xml2js shares sax. saxes and sax share historical fork lineage but have distinct parser code. fast-xml-parser has its own scanner and validator but no namespace URI resolution, so the adapter resolves expanded names over its qualified names and xmlns attributes. @xmldom/xmldom has its own XMLReader tokenizer and DOM builder, accepts locally decoded text, and the adapter treats every warning or error as fatal. jsdom builds its XML DOM over the same pinned saxes 6.0.0 tokenizer as the selected saxes path; it copies DOCTYPE entity declarations into saxes and forces XML 1.0 rules, and its AFL++ feedback includes input-independent window setup alongside saxes and DOM construction. xml2js, xml-js and xmldoc build distinct trees over the same pinned sax 1.6.1 tokenizer as the selected sax path; it drops comments and processing instructions, which can merge adjacent text segments. Wrapper package and underlying tokenizer source coverage are recorded separately. xmlbuilder2 4.0.3 is excluded from this namespace-aware selection: its native DOM misassigns the c:catalog and c:lang namespace URIs on the valid catalog control; the adapter does not repair them. htmlparser2 xmlMode has its own forgiving tokenizer but no XML well-formedness or namespace-URI enforcement; it is selected only as a raw-name XML event path, and its 526,964,241 downloads mostly measure HTML use. xmldoc builds a raw-name tree over sax; it omits prolog comments and PIs. Both are compared only to a non-namespace Expat oracle projected to preserved fields, without adapter-side namespace repair. The search is bounded to recorded queries and snapshot; two valid controls do not establish complete XML 1.0 compliance.

[Ranking and search limits](../../../data/javascript/xml/ranking.md) · [Standard API inventory](../../../data/javascript/xml/standard.json)

## Third-party parsers

- [saxes](saxes/README.md) — verified Docker harness
- [jsdom](jsdom/README.md) — verified Docker harness
- [htmlparser2](htmlparser2/README.md) — verified Docker harness
- [sax](sax/README.md) — verified Docker harness
- [fast-xml-parser](fast-xml-parser/README.md) — verified Docker harness
- [@xmldom/xmldom](xmldom-xmldom/README.md) — verified Docker harness
- [xml2js](xml2js/README.md) — verified Docker harness
- [xml-js](xml-js/README.md) — verified Docker harness
- [xmldoc](xmldoc/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
