# github.com/moovweb/gokogiri/xml — XML / Go

Pinned release: `v0.0.0-20180713195410-a1a828153468`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/go/github-com-moovweb-gokogiri-xml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml go github_com_moovweb_gokogiri
python3 parsarium.py run xml go github_com_moovweb_gokogiri controls/xml/catalog-ns.xml
python3 parsarium.py replay xml go github_com_moovweb_gokogiri CORPUS_DIR runs/xml-github_com_moovweb_gokogiri-replay
python3 parsarium.py afl build xml go github_com_moovweb_gokogiri
python3 parsarium.py afl prepare xml go github_com_moovweb_gokogiri runs/xml-github_com_moovweb_gokogiri-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Only two valid UTF-8 XML controls without DOCTYPE; compatibility patch updates 2018 cgo syntax/includes and a removed libxml2 debug helper. No malformed input, fuzzing campaign, DTD, XML 1.1, or non-UTF-8 validation.
