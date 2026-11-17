# mellium.im/xmlstream lead check — Go / XML

This is a reproducible **negative lead probe**, not a Parsarium parser project. Pinned `v0.15.4` has no API that takes local XML bytes and returns parsed structure, and it has no tokenizer. `ReadAll`, `NewIter` and the other token helpers read from an `xml.TokenReader` that the caller builds with `encoding/xml.NewDecoder`. The one `io.Reader` API, `InnerReader`, decodes only the outer element and returns the inner bytes unparsed.

The probe runs three paths on both valid controls inside the pinned Go 1.27.1 image:

- `readall`: `xmlstream.ReadAll(xml.NewDecoder(r))`
- `iter`: a recursive `xmlstream.NewIter` walk under the root
- `innerreader`: `xmlstream.InnerReader(r)` from the root start tag

`readall` and `iter` match the shared namespace-aware result exactly. Both controls run the same xmlstream cover blocks, and every block that differs is in `encoding/xml`. That is the stdlib decoder Parsarium already counts, so I record xmlstream as a negative lead and do not count it.

From the repository root:

```sh
python3 lead-probes/go/xml/xmlstream/check.py
```

The command checks the module archive, LICENSE and `encoding/xml/xml.go` hashes, repeats every run, and writes [the observation](../../../../data/go/xml/xmlstream-lead-check.json). It needs network access inside the container for `go mod download`. It does not run a malformed-input probe or a fuzz campaign.
