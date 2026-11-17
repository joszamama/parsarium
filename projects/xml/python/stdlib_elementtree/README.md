# ElementTree — XML / Python standard library

Pinned runtime: CPython `3.14.4` and Expat `2.10.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Official API, control result, and parser family](../../../../catalog/xml/python/stdlib_elementtree/README.md)

Run from the repository root:

```sh
python3 parsarium.py build xml python stdlib_elementtree
python3 parsarium.py run xml python stdlib_elementtree controls/xml/two-items.xml
python3 parsarium.py replay xml python stdlib_elementtree CORPUS_DIR runs/xml-elementtree-replay
python3 parsarium.py afl build xml python stdlib_elementtree
python3 parsarium.py afl prepare xml python stdlib_elementtree runs/xml-elementtree-afl
```

`CORPUS_DIR` contains XML files for one-file replay. AFL++ preparation writes a run plan and seeds; it does not start a campaign.
