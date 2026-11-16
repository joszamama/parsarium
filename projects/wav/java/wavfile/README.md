# wavfile — WAV / Java

Pinned release: `1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/wavfile/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java wavfile
python3 parsarium.py run wav java wavfile controls/wav/256-samples.wav
python3 parsarium.py replay wav java wavfile CORPUS_DIR runs/wav-wavfile-replay
python3 parsarium.py afl build wav java wavfile
python3 parsarium.py afl prepare wav java wavfile runs/wav-wavfile-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
