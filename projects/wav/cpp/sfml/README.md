# sfml — WAV / C++

Pinned release: `3.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/cpp/sfml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav cpp sfml
python3 parsarium.py run wav cpp sfml controls/wav/four-samples.wav
python3 parsarium.py replay wav cpp sfml CORPUS_DIR runs/wav-sfml-replay
python3 parsarium.py afl build wav cpp sfml
python3 parsarium.py afl prepare wav cpp sfml runs/wav-sfml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
