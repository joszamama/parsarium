# jdk-imageicon — PNG / Java

Pinned release: `21.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/java/png/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build png java jdk_imageicon
python3 parsarium.py run png java jdk_imageicon controls/png/red-green.png
python3 parsarium.py replay png java jdk_imageicon CORPUS_DIR runs/png-jdk_imageicon-replay
python3 parsarium.py afl build png java jdk_imageicon
python3 parsarium.py afl prepare png java jdk_imageicon runs/png-jdk_imageicon-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
