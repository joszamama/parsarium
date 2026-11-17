# github.com/segmentio/encoding/json — JSON / Go

Pinned release: `v0.5.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/go/github-com-segmentio-encoding-json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json go segmentio_encoding
python3 parsarium.py run json go segmentio_encoding controls/json/nested-object.json
python3 parsarium.py replay json go segmentio_encoding CORPUS_DIR runs/json-segmentio_encoding-replay
python3 parsarium.py afl build json go segmentio_encoding
python3 parsarium.py afl prepare json go segmentio_encoding runs/json-segmentio_encoding-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
