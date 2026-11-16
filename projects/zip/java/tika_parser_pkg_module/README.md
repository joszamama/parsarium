# tika-parser-pkg-module — ZIP / Java

Pinned release: `4.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/tika-parser-pkg-module/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java tika_parser_pkg_module
python3 parsarium.py run zip java tika_parser_pkg_module controls/zip/hello.zip
python3 parsarium.py replay zip java tika_parser_pkg_module CORPUS_DIR runs/zip-tika_parser_pkg_module-replay
python3 parsarium.py afl build zip java tika_parser_pkg_module
python3 parsarium.py afl prepare zip java tika_parser_pkg_module runs/zip-tika_parser_pkg_module-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
