# libaudiofile — WAV / C++

Pinned release: `0.3.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/cpp/libaudiofile/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav cpp libaudiofile
python3 parsarium.py run wav cpp libaudiofile controls/wav/four-samples.wav
python3 parsarium.py replay wav cpp libaudiofile CORPUS_DIR runs/wav-libaudiofile-replay
python3 parsarium.py afl build wav cpp libaudiofile
python3 parsarium.py afl prepare wav cpp libaudiofile runs/wav-libaudiofile-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
