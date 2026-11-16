# jaudiotagger — WAV / Java

Pinned release: `3.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/jaudiotagger/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java jaudiotagger
python3 parsarium.py run wav java jaudiotagger controls/wav/256-samples.wav
python3 parsarium.py replay wav java jaudiotagger CORPUS_DIR runs/wav-jaudiotagger-replay
python3 parsarium.py afl build wav java jaudiotagger
python3 parsarium.py afl prepare wav java jaudiotagger runs/wav-jaudiotagger-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
