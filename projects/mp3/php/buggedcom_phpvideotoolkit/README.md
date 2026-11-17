# buggedcom/phpvideotoolkit — MP3 / PHP

Pinned release: `2.2.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/php/buggedcom-phpvideotoolkit/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 php buggedcom_phpvideotoolkit
python3 parsarium.py run mp3 php buggedcom_phpvideotoolkit controls/mp3/id3v2-tagged-tone.mp3
python3 parsarium.py replay mp3 php buggedcom_phpvideotoolkit CORPUS_DIR runs/mp3-buggedcom_phpvideotoolkit-replay
python3 parsarium.py afl build mp3 php buggedcom_phpvideotoolkit
python3 parsarium.py afl prepare mp3 php buggedcom_phpvideotoolkit runs/mp3-buggedcom_phpvideotoolkit-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
