# freealut — WAV / C++

Pinned release: `1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/cpp/freealut/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav cpp freealut
python3 parsarium.py run wav cpp freealut controls/wav/four-samples.wav
python3 parsarium.py replay wav cpp freealut CORPUS_DIR runs/wav-freealut-replay
python3 parsarium.py afl build wav cpp freealut
python3 parsarium.py afl prepare wav cpp freealut runs/wav-freealut-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
