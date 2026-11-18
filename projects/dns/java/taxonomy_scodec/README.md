# taxonomy-scodec_2.13 — DNS / Java

Pinned release: `1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/java/taxonomy-scodec-2-13/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns java taxonomy_scodec
python3 parsarium.py run dns java taxonomy_scodec controls/dns/response.bin
python3 parsarium.py replay dns java taxonomy_scodec CORPUS_DIR runs/dns-taxonomy_scodec-replay
python3 parsarium.py afl build dns java taxonomy_scodec
python3 parsarium.py afl prepare dns java taxonomy_scodec runs/dns-taxonomy_scodec-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
