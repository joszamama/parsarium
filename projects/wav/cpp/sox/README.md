# sox — WAV / C++

Pinned release: `14.4.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/cpp/sox/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav cpp sox
python3 parsarium.py run wav cpp sox controls/wav/four-samples.wav
python3 parsarium.py replay wav cpp sox CORPUS_DIR runs/wav-sox-replay
python3 parsarium.py afl build wav cpp sox
python3 parsarium.py afl prepare wav cpp sox runs/wav-sox-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
