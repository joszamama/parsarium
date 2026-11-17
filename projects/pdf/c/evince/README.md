# evince — PDF / C

Pinned release: `48.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/c/evince/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf c evince
python3 parsarium.py run pdf c evince controls/pdf/two-page.pdf
python3 parsarium.py replay pdf c evince CORPUS_DIR runs/pdf-evince-replay
python3 parsarium.py afl build pdf c evince
python3 parsarium.py afl prepare pdf c evince runs/pdf-evince-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
