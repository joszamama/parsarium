# soluble/mediatools — MP4 / PHP

Pinned release: `2.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/php/soluble-mediatools/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 php soluble_mediatools
python3 parsarium.py run mp4 php soluble_mediatools controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 php soluble_mediatools CORPUS_DIR runs/mp4-soluble_mediatools-replay
python3 parsarium.py afl build mp4 php soluble_mediatools
python3 parsarium.py afl prepare mp4 php soluble_mediatools runs/mp4-soluble_mediatools-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
