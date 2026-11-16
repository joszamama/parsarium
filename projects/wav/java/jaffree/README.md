# jaffree — WAV / Java

Pinned release: `2024.08.29`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/jaffree/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java jaffree
python3 parsarium.py run wav java jaffree controls/wav/256-samples.wav
python3 parsarium.py replay wav java jaffree CORPUS_DIR runs/wav-jaffree-replay
python3 parsarium.py afl build wav java jaffree
python3 parsarium.py afl prepare wav java jaffree runs/wav-jaffree-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
