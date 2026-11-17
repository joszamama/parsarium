# beautifulsoup4 — XML / Python

Pinned release: `4.15.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/python/beautifulsoup4/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml python beautifulsoup4
python3 parsarium.py run xml python beautifulsoup4 controls/xml/catalog-ns.xml
python3 parsarium.py replay xml python beautifulsoup4 CORPUS_DIR runs/xml-beautifulsoup4-replay
python3 parsarium.py afl build xml python beautifulsoup4
python3 parsarium.py afl prepare xml python beautifulsoup4 runs/xml-beautifulsoup4-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
