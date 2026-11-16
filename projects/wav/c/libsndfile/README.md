# libsndfile — WAV / C

Pinned release: `1.2.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/c/libsndfile/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav c libsndfile
python3 parsarium.py run wav c libsndfile controls/wav/four-samples.wav
python3 parsarium.py replay wav c libsndfile CORPUS_DIR runs/wav-libsndfile-replay
python3 parsarium.py afl build wav c libsndfile
python3 parsarium.py afl prepare wav c libsndfile runs/wav-libsndfile-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
