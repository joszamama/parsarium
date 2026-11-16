# sfml — PNG / C++

Pinned release: `3.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/cpp/sfml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png cpp sfml
python3 parsarium.py run png cpp sfml controls/png/red-green.png
python3 parsarium.py replay png cpp sfml CORPUS_DIR runs/png-sfml-replay
python3 parsarium.py afl build png cpp sfml
python3 parsarium.py afl prepare png cpp sfml runs/png-sfml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
