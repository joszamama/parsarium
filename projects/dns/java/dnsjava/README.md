# dnsjava — DNS / Java

Pinned release: `3.7.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/java/dnsjava/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns java dnsjava
python3 parsarium.py run dns java dnsjava controls/dns/response.bin
python3 parsarium.py replay dns java dnsjava CORPUS_DIR runs/dns-dnsjava-replay
python3 parsarium.py afl build dns java dnsjava
python3 parsarium.py afl prepare dns java dnsjava runs/dns-dnsjava-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
