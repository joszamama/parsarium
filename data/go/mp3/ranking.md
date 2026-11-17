# Go plain MP3 parser pilot

The only verified third-party path in this pilot is
[`github.com/hajimehoshi/go-mp3`](../../../projects/mp3/go/github_com_hajimehoshi_go_mp3/README.md)
v0.3.4. Its documented `NewDecoder(io.Reader)` API decoded the untagged MPEG
Layer III controls. The package has **294 pkg.go.dev “Imported by” packages**
in the [saved search snapshot](registry-snapshot.json). This is a Go adoption
proxy, not a count of MP3 decoding users. The same decoder family is already
represented in the active tagged MP3 cell; the plain MP3 control is a distinct
format path, not an independent parser family.

Five pkg.go.dev queries were bounded at 100 hits each. The snapshot records
313 hits and 242 distinct package paths; [leads](leads.json) records 14
inspected candidates, including wrappers that share this decoder. Those leads
are not verified entries. This one-entry pilot is neither a top-ten ranking nor
evidence that only one Go parser exists. The [cell record](cell.json) gives the
remaining uncertainty and standard-library finding.
