# buggedcom/phpvideotoolkit — WAV / PHP

Pinned release: `2.2.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/buggedcom-phpvideotoolkit/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php buggedcom_phpvideotoolkit
python3 parsarium.py run wav php buggedcom_phpvideotoolkit controls/wav/256-samples.wav
python3 parsarium.py replay wav php buggedcom_phpvideotoolkit CORPUS_DIR runs/wav-buggedcom_phpvideotoolkit-replay
python3 parsarium.py afl build wav php buggedcom_phpvideotoolkit
python3 parsarium.py afl prepare wav php buggedcom_phpvideotoolkit runs/wav-buggedcom_phpvideotoolkit-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
