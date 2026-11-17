# xmltodict — XML / Python

Pinned release: `1.0.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/python/xmltodict/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml python xmltodict
python3 parsarium.py run xml python xmltodict controls/xml/two-items.xml
python3 parsarium.py replay xml python xmltodict CORPUS_DIR runs/xml-xmltodict-replay
python3 parsarium.py afl build xml python xmltodict
python3 parsarium.py afl prepare xml python xmltodict runs/xml-xmltodict-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
