# cpprestsdk — JSON / C++

Pinned release: `2.10.19`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/cpp/cpprestsdk/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json cpp cpprestsdk
python3 parsarium.py run json cpp cpprestsdk controls/json/nested-object.json
python3 parsarium.py replay json cpp cpprestsdk CORPUS_DIR runs/json-cpprestsdk-replay
python3 parsarium.py afl build json cpp cpprestsdk
python3 parsarium.py afl prepare json cpp cpprestsdk runs/json-cpprestsdk-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
