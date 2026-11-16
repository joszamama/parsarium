# soluble/mediatools — WAV / PHP

Pinned release: `2.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/soluble-mediatools/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php soluble_mediatools
python3 parsarium.py run wav php soluble_mediatools controls/wav/256-samples.wav
python3 parsarium.py replay wav php soluble_mediatools CORPUS_DIR runs/wav-soluble_mediatools-replay
python3 parsarium.py afl build wav php soluble_mediatools
python3 parsarium.py afl prepare wav php soluble_mediatools runs/wav-soluble_mediatools-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
