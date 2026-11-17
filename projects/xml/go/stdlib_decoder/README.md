# encoding/xml.Decoder.Token() — XML / Go

Pinned release: `1.27.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/go/xml/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build xml go stdlib_decoder
python3 parsarium.py run xml go stdlib_decoder controls/xml/catalog-ns.xml
python3 parsarium.py replay xml go stdlib_decoder CORPUS_DIR runs/xml-stdlib_decoder-replay
python3 parsarium.py afl build xml go stdlib_decoder
python3 parsarium.py afl prepare xml go stdlib_decoder runs/xml-stdlib_decoder-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
