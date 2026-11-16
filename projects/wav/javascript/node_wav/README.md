# node-wav — WAV / JavaScript

Pinned release: `0.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/javascript/node-wav/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav javascript node_wav
python3 parsarium.py run wav javascript node_wav controls/wav/four-samples.wav
python3 parsarium.py replay wav javascript node_wav CORPUS_DIR runs/wav-node_wav-replay
python3 parsarium.py afl build wav javascript node_wav
python3 parsarium.py afl prepare wav javascript node_wav runs/wav-node_wav-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
