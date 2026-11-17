# libtins — DNS / C++

Pinned release: `4.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/cpp/libtins/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns cpp libtins
python3 parsarium.py run dns cpp libtins controls/dns/response.bin
python3 parsarium.py replay dns cpp libtins CORPUS_DIR runs/dns-libtins-replay
python3 parsarium.py afl build dns cpp libtins
python3 parsarium.py afl prepare dns cpp libtins runs/dns-libtins-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
