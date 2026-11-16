# jdk-jarinputstream — ZIP / Java

Pinned release: `21.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/java/zip/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build zip java jdk_jarinputstream
python3 parsarium.py run zip java jdk_jarinputstream controls/zip/hello.zip
python3 parsarium.py replay zip java jdk_jarinputstream CORPUS_DIR runs/zip-jdk_jarinputstream-replay
python3 parsarium.py afl build zip java jdk_jarinputstream
python3 parsarium.py afl prepare zip java jdk_jarinputstream runs/zip-jdk_jarinputstream-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
