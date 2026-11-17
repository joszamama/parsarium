# pydantic — JSON / Python

Pinned release: `2.14.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/python/pydantic/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json python pydantic
python3 parsarium.py run json python pydantic controls/json/structure.json
python3 parsarium.py replay json python pydantic CORPUS_DIR runs/json-pydantic-replay
python3 parsarium.py afl build json python pydantic
python3 parsarium.py afl prepare json python pydantic runs/json-pydantic-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
