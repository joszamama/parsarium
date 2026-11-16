# codecmedia — WAV / Java

Pinned release: `1.2.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/codecmedia/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java codecmedia
python3 parsarium.py run wav java codecmedia controls/wav/256-samples.wav
python3 parsarium.py replay wav java codecmedia CORPUS_DIR runs/wav-codecmedia-replay
python3 parsarium.py afl build wav java codecmedia
python3 parsarium.py afl prepare wav java codecmedia runs/wav-codecmedia-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
