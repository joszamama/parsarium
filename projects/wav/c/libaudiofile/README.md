# libaudiofile — WAV / C

Pinned release: `0.3.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/c/libaudiofile/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav c libaudiofile
python3 parsarium.py run wav c libaudiofile controls/wav/four-samples.wav
python3 parsarium.py replay wav c libaudiofile CORPUS_DIR runs/wav-libaudiofile-replay
python3 parsarium.py afl build wav c libaudiofile
python3 parsarium.py afl prepare wav c libaudiofile runs/wav-libaudiofile-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
