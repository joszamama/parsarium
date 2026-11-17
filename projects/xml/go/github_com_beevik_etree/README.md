# github.com/beevik/etree — XML / Go

Pinned release: `v1.8.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/go/github-com-beevik-etree/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml go github_com_beevik_etree
python3 parsarium.py run xml go github_com_beevik_etree controls/xml/catalog-ns.xml
python3 parsarium.py replay xml go github_com_beevik_etree CORPUS_DIR runs/xml-github_com_beevik_etree-replay
python3 parsarium.py afl build xml go github_com_beevik_etree
python3 parsarium.py afl prepare xml go github_com_beevik_etree runs/xml-github_com_beevik_etree-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
