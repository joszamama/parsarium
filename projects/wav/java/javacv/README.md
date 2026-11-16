# javacv — WAV / Java

Pinned release: `1.5.14`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/javacv/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java javacv
python3 parsarium.py run wav java javacv controls/wav/256-samples.wav
python3 parsarium.py replay wav java javacv CORPUS_DIR runs/wav-javacv-replay
python3 parsarium.py afl build wav java javacv
python3 parsarium.py afl prepare wav java javacv runs/wav-javacv-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
