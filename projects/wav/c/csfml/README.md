# csfml — WAV / C

Pinned release: `3.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/c/csfml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav c csfml
python3 parsarium.py run wav c csfml controls/wav/four-samples.wav
python3 parsarium.py replay wav c csfml CORPUS_DIR runs/wav-csfml-replay
python3 parsarium.py afl build wav c csfml
python3 parsarium.py afl prepare wav c csfml runs/wav-csfml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
