# jave-core — WAV / Java

Pinned release: `4.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/jave-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java jave_core
python3 parsarium.py run wav java jave_core controls/wav/256-samples.wav
python3 parsarium.py replay wav java jave_core CORPUS_DIR runs/wav-jave_core-replay
python3 parsarium.py afl build wav java jave_core
python3 parsarium.py afl prepare wav java jave_core runs/wav-jave_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
