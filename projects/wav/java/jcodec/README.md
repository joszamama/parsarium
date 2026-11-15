# jcodec — WAV / Java

Pinned release: `0.2.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/jcodec/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java jcodec
python3 parsarium.py run wav java jcodec controls/wav/256-samples.wav
python3 parsarium.py replay wav java jcodec CORPUS_DIR runs/wav-jcodec-replay
python3 parsarium.py afl build wav java jcodec
python3 parsarium.py afl prepare wav java jcodec runs/wav-jcodec-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
