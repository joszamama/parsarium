# miniaudio — WAV / C++

Pinned release: `0.11.26`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/cpp/miniaudio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav cpp miniaudio
python3 parsarium.py run wav cpp miniaudio controls/wav/four-samples.wav
python3 parsarium.py replay wav cpp miniaudio CORPUS_DIR runs/wav-miniaudio-replay
python3 parsarium.py afl build wav cpp miniaudio
python3 parsarium.py afl prepare wav cpp miniaudio runs/wav-miniaudio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
