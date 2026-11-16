# poco — ZIP / C++

Pinned release: `1.15.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/poco/README.md)

The harness reads the archive from an in-memory `std::istringstream` with `Poco::Zip::ZipArchive`, then decompresses the first entry with `Poco::Zip::ZipInputStream` and checks its CRC. Poco and its bundled zlib 1.3.2 are built from the pinned release archive.

Harness caps: input up to 1 MiB, entry name up to 64 KiB, decompressed content up to 1 MiB. Inputs past a cap are rejected.

The pinned Docker control found one `hello.txt` entry and decompressed `parsarium\n`. LLVM coverage reached 329 Poco ZIP source lines and 369 bundled zlib source lines; AFL++ produced 783 feedback edges.

## Run from the repository root

```sh
python3 parsarium.py build zip cpp poco
python3 parsarium.py run zip cpp poco controls/zip/hello.zip
python3 parsarium.py replay zip cpp poco CORPUS_DIR runs/zip-poco-replay
python3 parsarium.py afl build zip cpp poco
python3 parsarium.py afl prepare zip cpp poco runs/zip-poco-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
