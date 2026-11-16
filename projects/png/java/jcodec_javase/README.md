# jcodec-javase — PNG / Java

Pinned release: `0.2.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/jcodec-javase/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java jcodec_javase
python3 parsarium.py run png java jcodec_javase controls/png/red-green.png
python3 parsarium.py replay png java jcodec_javase CORPUS_DIR runs/png-jcodec_javase-replay
python3 parsarium.py afl build png java jcodec_javase
python3 parsarium.py afl prepare png java jcodec_javase runs/png-jcodec_javase-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
