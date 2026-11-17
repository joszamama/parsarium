# parsel — XML / Python

Pinned release: `1.12.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/python/parsel/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml python parsel
python3 parsarium.py run xml python parsel controls/xml/catalog-ns.xml
python3 parsarium.py replay xml python parsel CORPUS_DIR runs/xml-parsel-replay
python3 parsarium.py afl build xml python parsel
python3 parsarium.py afl prepare xml python parsel runs/xml-parsel-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
