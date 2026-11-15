# riffy — WAV / Python

Pinned release: `0.3.16`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/riffy/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python riffy
python3 parsarium.py run wav python riffy controls/wav/four-samples.wav
python3 parsarium.py replay wav python riffy CORPUS_DIR runs/wav-riffy-replay
python3 parsarium.py afl build wav python riffy
python3 parsarium.py afl prepare wav python riffy runs/wav-riffy-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
