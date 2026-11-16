# beads — WAV / Java

Pinned release: `3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/beads/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java beads
python3 parsarium.py run wav java beads controls/wav/256-samples.wav
python3 parsarium.py replay wav java beads CORPUS_DIR runs/wav-beads-replay
python3 parsarium.py afl build wav java beads
python3 parsarium.py afl prepare wav java beads runs/wav-beads-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
