# github.com/antchfx/xmlquery — XML / Go

Pinned release: `v1.5.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/go/github-com-antchfx-xmlquery/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml go github_com_antchfx_xmlquery
python3 parsarium.py run xml go github_com_antchfx_xmlquery controls/xml/catalog-ns.xml
python3 parsarium.py replay xml go github_com_antchfx_xmlquery CORPUS_DIR runs/xml-github_com_antchfx_xmlquery-replay
python3 parsarium.py afl build xml go github_com_antchfx_xmlquery
python3 parsarium.py afl prepare xml go github_com_antchfx_xmlquery runs/xml-github_com_antchfx_xmlquery-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
