# buggedcom/phpvideotoolkit — MP4 / PHP

Pinned release: `2.2.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/php/buggedcom-phpvideotoolkit/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 php buggedcom_phpvideotoolkit
python3 parsarium.py run mp4 php buggedcom_phpvideotoolkit controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 php buggedcom_phpvideotoolkit CORPUS_DIR runs/mp4-buggedcom_phpvideotoolkit-replay
python3 parsarium.py afl build mp4 php buggedcom_phpvideotoolkit
python3 parsarium.py afl prepare mp4 php buggedcom_phpvideotoolkit runs/mp4-buggedcom_phpvideotoolkit-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
