# bit7z — ZIP / C++

Pinned release: `4.1.0`, over SevenZip `26.04`. [Manifest](manifest.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/bit7z/README.md)

The valid ZIP control passed Docker replay and one-case fuzzer smoke. Coverage reached 594 bit7z lines and 2,750 underlying SevenZip lines, including 756 ZIP reader, 282 ZIP handler, and 160 Deflate decoder lines. The AFL++ overlay recorded 1,535 feedback edges on the same control. [Docker receipt](verification.json) and [AFL++ receipt](../../../../fuzzing/afl-native/zip/cpp/bit7z/verification.json) bind the builds and control. A valid empty ZIP also parses with zero entries.

The pinned SevenZip source performs unaligned integer loads on the valid control, so the fuzzer disables UBSan's alignment check. The AFL++ compiler wrapper additionally needs UBSan's function-type check disabled. bit7z and SevenZip define duplicate COM GUID constants, so ASan's duplicate-global ODR check is disabled at load. ASan memory checks and the remaining UBSan checks stay enabled; no upstream source is patched.

The image builds both libraries from their pinned sources: the bit7z static library and the SevenZip `Format7zF` `7z.so` that bit7z loads. Coverage is gated on bit7z's reader and buffer extraction sources and on SevenZip's ZIP handler, ZIP reader, and Deflate decoder. bit7z and SevenZip are one parser family.

The harness caps input at 1 MiB and decoded content at 1 MiB. SevenZip does not limit output for entries with a data descriptor, so the harness aborts extraction through bit7z's progress callback. The abort takes effect at the decoder's next progress report, which for Deflate comes every 1 MiB of output.

## Run from the repository root

```sh
python3 parsarium.py build zip cpp bit7z
python3 parsarium.py run zip cpp bit7z controls/zip/hello.zip
python3 parsarium.py replay zip cpp bit7z CORPUS_DIR runs/zip-bit7z-replay
python3 parsarium.py afl build zip cpp bit7z
python3 parsarium.py afl prepare zip cpp bit7z runs/zip-bit7z-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
