# ant — ZIP / Java

Pinned release: `1.10.18`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/ant/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java ant
python3 parsarium.py run zip java ant controls/zip/hello.zip
python3 parsarium.py replay zip java ant CORPUS_DIR runs/zip-ant-replay
python3 parsarium.py afl build zip java ant
python3 parsarium.py afl prepare zip java ant runs/zip-ant-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
