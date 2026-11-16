# v47-jaffree — WAV / Java

Pinned release: `2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/v47-jaffree/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java v47_jaffree
python3 parsarium.py run wav java v47_jaffree controls/wav/256-samples.wav
python3 parsarium.py replay wav java v47_jaffree CORPUS_DIR runs/wav-v47_jaffree-replay
python3 parsarium.py afl build wav java v47_jaffree
python3 parsarium.py afl prepare wav java v47_jaffree runs/wav-v47_jaffree-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
