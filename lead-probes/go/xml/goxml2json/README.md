# goxml2json lead check — Go / XML

This is a reproducible **unselected lead probe**, not a Parsarium parser project. The pinned v1.1.0 `Convert(io.Reader)` API transforms each valid XML control to JSON. The output drops namespace URIs from element and attribute names, so it cannot meet the shared namespace-aware XML result without reading the raw XML separately.

From the repository root:

```sh
python3 lead-probes/go/xml/goxml2json/check.py
```

The command verifies the module archive SHA-256, runs both valid controls, and writes [the observation](../../../../data/go/xml/goxml2json-lead-check.json). It does not run a malformed-input probe or a fuzz campaign.
