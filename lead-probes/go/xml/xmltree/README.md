# aqwari.net/xml/xmltree lead check — Go / XML

This is a reproducible **negative lead probe**, not a Parsarium parser project. The API works: `xmltree.Parse([]byte)` parses both valid controls, and its tree matches an independent oracle exactly. It fails the cell's feedback gate. On the fixed control pair, the package's own source gives the same AFL++ map, and every difference is in Go `encoding/xml`.

Pinned module `aqwari.net/xml v0.0.0-20210331023308-d9421b293817` (upstream `github.com/droyo/go-xml` commit `d9421b293817`, MIT). There is no tagged release. The [source lock](source-lock.json) records the module zip, `go.sum` hash, LICENSE and `xmltree.go` hashes, plus the zip hashes of `golang.org/x/net` and `golang.org/x/text`. The [Dockerfile](Dockerfile) checks all of them, along with `encoding/xml/xml.go`.

## API and parser family

- Input: `xmltree.Parse(doc []byte) (*Element, error)`. There is no `io.Reader` or file entry point.
- Parsing: `Parse` creates `encoding/xml.NewDecoder(bytes.NewReader(doc))` and builds `Element` values from `Token()`. Lexing, references, CDATA, attribute values and namespace resolution of names all run in `encoding/xml`. xmltree shares the Go `encoding/xml` Decoder family with `stdlib_decoder`, etree, xmlquery, mxj, x2j and goxpp. It is not an independent engine.
- xmltree's own code: the tree walk, a namespace-scope stack (`pushNS`), `Scope.Prefix`/`Resolve`, and `Content` slicing by `Decoder.InputOffset`.
- `golang.org/x/net/html/charset` is linked, but it only runs for non-UTF-8 encoding labels.

## What the tree exposes

The [harness](harness.go) reports the tree as xmltree returns it and does not repair anything:

- expanded element and attribute names in document order
- qualified names rebuilt by `Scope.Prefix`
- maximum depth
- URIs used in names
- raw `Content` of each leaf element

xmltree keeps no decoded text. `Content` holds the source bytes between the tags, so `Café &amp; té`, `A&#x2D;7` and `<![CDATA[x < y]]>` come back as written. Namespace declarations move into an unexported `Scope`, so they can be resolved but not listed or counted.

The [oracle](oracle.py) uses Python expat in namespace mode with prefixes enabled. It slices raw leaf bytes at expat's byte offsets. It matches xmltree exactly on `catalog-ns.xml` and `order-default-ns.xml`, including `xmlns=""` on `<plain>`.

## Observed result

| | catalog-ns.xml | order-default-ns.xml |
|---|---|---|
| xmltree.go cover blocks / lines | 42 / 54 | 42 / 54 |
| encoding/xml cover blocks / lines | 179 / 293 | 195 / 327 |
| xmltree-scoped AFL++ features / tuples | 42 / 62 | 42 / 62 |

Repeats are identical. On this pair, xmltree's blocks and AFL++ map differ by 0. `encoding/xml` differs by 30 features and 30 tuples. That is the gate that excluded `mellium.im/xmlstream`, so I do not count xmltree.

The feedback does depend on input. `one-item.xml` and `two-items.xml` have a single default declaration, and each one changes four `xmltree.go` blocks: the declaration sort, the prefixed `pushNS` branch and the prefixed `Prefix` branch. I record that as supplementary evidence. It does not replace the fixed differential.

Metric: pkg.go.dev reports 43 importing packages from 20 modules, both in the registry snapshot and in a 14:30 UTC recheck. Of the 70 listed package paths, 58 are packages inside copies of the go-xml repository itself.

## Reproduce

From the repository root:

```sh
python3 lead-probes/go/xml/xmltree/check.py
```

The script builds the probe image, which needs network access for `go mod download`. It also builds the AFL++ bridge from [afl.Dockerfile](afl.Dockerfile), which uses the same `fuzzing/afl-bridge` files as Go projects. It replays both controls twice, compares them with the oracle, probes the AFL++ maps and writes [the observation](../../../../data/go/xml/xmltree-lead-check.json). It does not run malformed inputs or a fuzz campaign.
