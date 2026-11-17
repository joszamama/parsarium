# saxes — XML / JavaScript

Pinned release: `6.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Selection, leads, and standard API inventory](../../../../data/javascript/xml/ranking.md)

## Run from the repository root

```sh
python3 parsarium.py build xml javascript saxes
python3 parsarium.py run xml javascript saxes controls/xml/catalog-ns.xml
python3 parsarium.py replay xml javascript saxes CORPUS_DIR runs/xml-saxes-replay
python3 parsarium.py afl build xml javascript saxes
python3 parsarium.py afl prepare xml javascript saxes runs/xml-saxes-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
