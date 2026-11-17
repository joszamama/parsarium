# prewk/xml-string-streamer lead check — PHP / XML

This is a reproducible **negative lead probe**, not a Parsarium parser project. The pinned 1.2.3 `XmlStringStreamer::getNode()` streams a local file path, file handle or stdin and returns the next "node" as a string. Both splitters work on bytes: StringWalker finds tags with `preg_match('/<[^>]+>/')` and counts depth, and UniqueNode searches for `<name` and `</name>`. The returned strings are verbatim slices of the input. Names, attributes, text and namespaces are never read, entity references stay undecoded, and the release calls no XML parser. The README hands each node to `simplexml_load_string`. Under PROTOCOL.md this is byte copying, not a parser.

From the repository root:

```sh
python3 lead-probes/php/xml/prewk_xml_string_streamer/check.py
```

The command builds the pinned Docker image, which checks the source archive SHA-256 and diffs it against the Composer install. It then streams `catalog-ns.xml` and `order-default-ns.xml` through `createStringWalkerParser(path)`, StringWalker over a 7-byte `Stream\File` handle, and `createUniqueNodeParser(path)` under Xdebug. It compares every returned node byte-for-byte with an independent expat byte-span oracle. For each node it records the namespace bindings the node's names use that are declared outside the returned bytes. It writes [the observation](../../../../data/php/xml/prewk-xml-string-streamer-lead-check.json). It does not run malformed inputs, a fuzz campaign or an AFL++ bridge, because libxml2 is never called by this package.
