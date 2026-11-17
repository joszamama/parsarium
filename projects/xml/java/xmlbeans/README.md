# xmlbeans — XML / Java

Pinned release: `5.4.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/java/xmlbeans/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml java xmlbeans
python3 parsarium.py run xml java xmlbeans controls/xml/catalog-ns.xml
python3 parsarium.py replay xml java xmlbeans CORPUS_DIR runs/xml-xmlbeans-replay
python3 parsarium.py afl build xml java xmlbeans
python3 parsarium.py afl prepare xml java xmlbeans runs/xml-xmlbeans-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
