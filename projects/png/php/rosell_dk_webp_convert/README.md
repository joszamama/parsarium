# rosell-dk/webp-convert — PNG / PHP

Pinned release: `2.9.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/rosell-dk-webp-convert/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php rosell_dk_webp_convert
python3 parsarium.py run png php rosell_dk_webp_convert controls/png/red-green.png
python3 parsarium.py replay png php rosell_dk_webp_convert CORPUS_DIR runs/png-rosell_dk_webp_convert-replay
python3 parsarium.py afl build png php rosell_dk_webp_convert
python3 parsarium.py afl prepare png php rosell_dk_webp_convert runs/png-rosell_dk_webp_convert-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
