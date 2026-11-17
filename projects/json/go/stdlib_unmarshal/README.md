# encoding/json.Unmarshal([]byte, any) — JSON / Go

Pinned release: `1.27.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/go/json/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build json go stdlib_unmarshal
python3 parsarium.py run json go stdlib_unmarshal controls/json/nested-object.json
python3 parsarium.py replay json go stdlib_unmarshal CORPUS_DIR runs/json-stdlib_unmarshal-replay
python3 parsarium.py afl build json go stdlib_unmarshal
python3 parsarium.py afl prepare json go stdlib_unmarshal runs/json-stdlib_unmarshal-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
