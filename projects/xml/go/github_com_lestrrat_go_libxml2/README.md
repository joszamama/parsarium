# github.com/lestrrat-go/libxml2 — XML / Go

Pinned release: `v0.0.0-20260709020957-3f0f7bd60b63`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/go/github-com-lestrrat-go-libxml2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml go github_com_lestrrat_go_libxml2
python3 parsarium.py run xml go github_com_lestrrat_go_libxml2 controls/xml/catalog-ns.xml
python3 parsarium.py replay xml go github_com_lestrrat_go_libxml2 CORPUS_DIR runs/xml-github_com_lestrrat_go_libxml2-replay
python3 parsarium.py afl build xml go github_com_lestrrat_go_libxml2
python3 parsarium.py afl prepare xml go github_com_lestrrat_go_libxml2 runs/xml-github_com_lestrrat_go_libxml2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Only two valid UTF-8 XML controls without DOCTYPE; compatibility patch changes one cgo variable type in clib.go (xmlParseInNodeContext list pointer) so the 2026-07 pseudo-version compiles against libxml2 2.15.4 headers. No malformed input, fuzzing campaign, DTD, XML 1.1, or non-UTF-8 validation.
