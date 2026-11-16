# jdsp — WAV / Java

Pinned release: `3.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/jdsp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java jdsp
python3 parsarium.py run wav java jdsp controls/wav/256-samples.wav
python3 parsarium.py replay wav java jdsp CORPUS_DIR runs/wav-jdsp-replay
python3 parsarium.py afl build wav java jdsp
python3 parsarium.py afl prepare wav java jdsp runs/wav-jdsp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
