# jdk-imagereader — PNG / Java

Pinned release: `21.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/java/png/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build png java jdk_imagereader
python3 parsarium.py run png java jdk_imagereader controls/png/red-green.png
python3 parsarium.py replay png java jdk_imagereader CORPUS_DIR runs/png-jdk_imagereader-replay
python3 parsarium.py afl build png java jdk_imagereader
python3 parsarium.py afl prepare png java jdk_imagereader runs/png-jdk_imagereader-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
