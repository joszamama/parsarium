# github.com/lestrrat-go/helium — XML / Go

Pinned release: `v0.11.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/go/github-com-lestrrat-go-helium/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml go github_com_lestrrat_go_helium
python3 parsarium.py run xml go github_com_lestrrat_go_helium controls/xml/catalog-ns.xml
python3 parsarium.py replay xml go github_com_lestrrat_go_helium CORPUS_DIR runs/xml-github_com_lestrrat_go_helium-replay
python3 parsarium.py afl build xml go github_com_lestrrat_go_helium
python3 parsarium.py afl prepare xml go github_com_lestrrat_go_helium runs/xml-github_com_lestrrat_go_helium-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
