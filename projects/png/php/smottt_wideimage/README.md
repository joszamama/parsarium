# smottt/wideimage — PNG / PHP

Pinned release: `1.1.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/smottt-wideimage/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php smottt_wideimage
python3 parsarium.py run png php smottt_wideimage controls/png/red-green.png
python3 parsarium.py replay png php smottt_wideimage CORPUS_DIR runs/png-smottt_wideimage-replay
python3 parsarium.py afl build png php smottt_wideimage
python3 parsarium.py afl prepare png php smottt_wideimage runs/png-smottt_wideimage-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
