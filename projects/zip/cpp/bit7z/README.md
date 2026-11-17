# bit7z — ZIP / C++

Pinned release: `4.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/bit7z/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip cpp bit7z
python3 parsarium.py run zip cpp bit7z controls/zip/hello.zip
python3 parsarium.py replay zip cpp bit7z CORPUS_DIR runs/zip-bit7z-replay
python3 parsarium.py afl build zip cpp bit7z
python3 parsarium.py afl prepare zip cpp bit7z runs/zip-bit7z-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Sanitizer exception:** SevenZip performs unaligned integer loads on the valid ZIP control, so the fuzzer disables only UBSan's alignment check. The AFL++ overlay also disables UBSan's function-type check for AFL's compiler wrapper. bit7z and SevenZip both define COM GUID constants, so ASan's duplicate-global ODR check is disabled at load; ASan memory checks and other UBSan checks remain enabled.
