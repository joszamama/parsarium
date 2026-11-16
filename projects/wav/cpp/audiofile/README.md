# audiofile — WAV / C++

Pinned release: `1.1.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/cpp/audiofile/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav cpp audiofile
python3 parsarium.py run wav cpp audiofile controls/wav/four-samples.wav
python3 parsarium.py replay wav cpp audiofile CORPUS_DIR runs/wav-audiofile-replay
python3 parsarium.py afl build wav cpp audiofile
python3 parsarium.py afl prepare wav cpp audiofile runs/wav-audiofile-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
