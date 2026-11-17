# xml.etree.ElementTree — XML / Python

Pinned release: `3.14.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/python/xml/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build xml python stdlib_elementtree
python3 parsarium.py run xml python stdlib_elementtree controls/xml/two-items.xml
python3 parsarium.py replay xml python stdlib_elementtree CORPUS_DIR runs/xml-stdlib_elementtree-replay
python3 parsarium.py afl build xml python stdlib_elementtree
python3 parsarium.py afl prepare xml python stdlib_elementtree runs/xml-stdlib_elementtree-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
