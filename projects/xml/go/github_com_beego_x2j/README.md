# github.com/beego/x2j — XML / Go

Pinned release: `v0.0.0-20131220205130-a0352aadc542`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/go/github-com-beego-x2j/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml go github_com_beego_x2j
python3 parsarium.py run xml go github_com_beego_x2j controls/xml/catalog-ns.xml
python3 parsarium.py replay xml go github_com_beego_x2j CORPUS_DIR runs/xml-github_com_beego_x2j-replay
python3 parsarium.py afl build xml go github_com_beego_x2j
python3 parsarium.py afl prepare xml go github_com_beego_x2j runs/xml-github_com_beego_x2j-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
