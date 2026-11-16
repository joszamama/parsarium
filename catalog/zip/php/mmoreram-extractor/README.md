# mmoreram/extractor — ZIP / PHP

- **Pinned release:** `1.2.1`
- **License:** MIT
- **Parsed scope:** entry name and decompressed entry bytes
- **Underlying family:** Mmoreram extractor over PHP ZipArchive
- **Local input API:** `Extractor::extractFromFile(local ZIP path); iterate returned Finder`
- **Documentation:** [API reference](<https://github.com/mmoreram/extractor/blob/0ca76992fab2573e2fe512d0ee2a4d45e936fee4/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/zip/parsers.json) · [control verification](../../../../data/php/zip/verification.json) · [within-ecosystem ranking](../../../../data/php/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "entries": 1,
  "name": "hello.txt",
  "content": "parsarium\n"
}
```

The ZIP adapter delegates archive parsing and extraction to PHP ZipArchive.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/php/mmoreram_extractor/README.md)

```sh
python3 parsarium.py build zip php mmoreram_extractor
python3 parsarium.py run zip php mmoreram_extractor controls/zip/hello.zip
```
