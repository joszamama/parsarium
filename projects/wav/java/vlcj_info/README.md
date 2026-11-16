# vlcj-info — WAV / Java

Pinned release: `2.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/vlcj-info/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java vlcj_info
python3 parsarium.py run wav java vlcj_info controls/wav/256-samples.wav
python3 parsarium.py replay wav java vlcj_info CORPUS_DIR runs/wav-vlcj_info-replay
python3 parsarium.py afl build wav java vlcj_info
python3 parsarium.py afl prepare wav java vlcj_info runs/wav-vlcj_info-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
