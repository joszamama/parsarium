# github.com/mmcdole/goxpp — XML / Go

Pinned release: `v1.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/go/github-com-mmcdole-goxpp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml go github_com_mmcdole_goxpp
python3 parsarium.py run xml go github_com_mmcdole_goxpp controls/xml/catalog-ns.xml
python3 parsarium.py replay xml go github_com_mmcdole_goxpp CORPUS_DIR runs/xml-github_com_mmcdole_goxpp-replay
python3 parsarium.py afl build xml go github_com_mmcdole_goxpp
python3 parsarium.py afl prepare xml go github_com_mmcdole_goxpp runs/xml-github_com_mmcdole_goxpp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
