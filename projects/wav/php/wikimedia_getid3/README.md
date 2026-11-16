# wikimedia/getid3 — WAV / PHP

Pinned release: `v2.0.0-beta5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/wikimedia-getid3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php wikimedia_getid3
python3 parsarium.py run wav php wikimedia_getid3 controls/wav/256-samples.wav
python3 parsarium.py replay wav php wikimedia_getid3 CORPUS_DIR runs/wav-wikimedia_getid3-replay
python3 parsarium.py afl build wav php wikimedia_getid3
python3 parsarium.py afl prepare wav php wikimedia_getid3 runs/wav-wikimedia_getid3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
