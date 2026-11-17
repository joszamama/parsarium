# github.com/mmcdole/goxpp — XML / Go

Pinned release: `v1.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, controls, and parser family](../../../../catalog/xml/go/github-com-mmcdole-goxpp/README.md)

This pull parser reads a local byte stream through `NewXMLPullParser(io.Reader, true, nil)` and `NextToken()`. It uses Go `encoding/xml.Decoder.Token()` for tokenization, then maintains its own cursor, depth and namespace state. Coverage and AFL++ feedback report both source scopes separately.

## Run from the repository root

```sh
python3 parsarium.py build xml go github_com_mmcdole_goxpp
python3 parsarium.py run xml go github_com_mmcdole_goxpp controls/xml/catalog-ns.xml
python3 parsarium.py run xml go github_com_mmcdole_goxpp controls/xml/order-default-ns.xml
python3 parsarium.py replay xml go github_com_mmcdole_goxpp CORPUS_DIR runs/xml-goxpp-replay
python3 parsarium.py afl build xml go github_com_mmcdole_goxpp
python3 parsarium.py afl prepare xml go github_com_mmcdole_goxpp runs/xml-goxpp-afl
python3 projects/xml/go/github_com_mmcdole_goxpp/verify-feedback.py
```

Replace `CORPUS_DIR` with a directory of XML files. The AFL++ command prepares a seeded run; it does not start a campaign.
