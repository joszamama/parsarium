# tinytag — WAV / Python

Pinned release: `2.3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/tinytag/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python tinytag
python3 parsarium.py run wav python tinytag controls/wav/four-samples.wav
python3 parsarium.py replay wav python tinytag CORPUS_DIR runs/wav-tinytag-replay
python3 parsarium.py afl build wav python tinytag
python3 parsarium.py afl prepare wav python tinytag runs/wav-tinytag-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
