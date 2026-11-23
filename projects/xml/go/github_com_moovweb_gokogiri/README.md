# github.com/moovweb/gokogiri/xml — XML / Go

Pinned release: `v0.0.0-20180713195410-a1a828153468`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/go/github-com-moovweb-gokogiri-xml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml go github_com_moovweb_gokogiri
python3 parsarium.py run xml go github_com_moovweb_gokogiri controls/xml/catalog-ns.xml
python3 parsarium.py replay xml go github_com_moovweb_gokogiri CORPUS_DIR runs/xml-github_com_moovweb_gokogiri-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build xml go github_com_moovweb_gokogiri
python3 parsarium.py afl prepare xml go github_com_moovweb_gokogiri runs/xml-github_com_moovweb_gokogiri-afl --fandango 100
python3 parsarium.py afl run runs/xml-github_com_moovweb_gokogiri-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** Only two valid UTF-8 XML controls without DOCTYPE; compatibility patch updates 2018 cgo syntax/includes and a removed libxml2 debug helper. No malformed input, fuzzing campaign, DTD, XML 1.1, or non-UTF-8 validation.
