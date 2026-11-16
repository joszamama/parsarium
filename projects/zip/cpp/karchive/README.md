# karchive — ZIP / C++

Pinned release: `6.31.0`. [Manifest](manifest.json) · [Docker receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/zip/cpp/karchive/verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/karchive/README.md)

The harness writes the input bytes to a temporary `.zip` file, opens it with `KZip(path).open(QIODevice::ReadOnly)`, lists the root directory with `KArchiveDirectory::entries`, and reports the entry count plus the name and `KArchiveFile::data` content of the first entry in sorted order. Inputs are capped at 1 MiB and decoded content at 1 MiB.

The image builds only the static KArchive library from the pinned source tarball, with LLVM coverage for replay and sanitizer instrumentation for the fuzzer. It uses ECM 6.31.0 from its pinned tarball, Qt 6.10.2 (`6.10.2+dfsg-7`, checked at build time) and zlib from Ubuntu 26.04. Qt and zlib are not instrumented, so coverage and fuzzing feedback cover KArchive source only.

The valid deflate ZIP control passed replay and one-case fuzzer smoke. It covered 668 KArchive source lines, including 237 lines in `kzip.cpp`, and the AFL++ overlay recorded 1,275 feedback edges on the same control.

## Run from the repository root

```sh
python3 parsarium.py build zip cpp karchive
python3 parsarium.py run zip cpp karchive controls/zip/hello.zip
python3 parsarium.py replay zip cpp karchive CORPUS_DIR runs/zip-karchive-replay
python3 parsarium.py afl build zip cpp karchive
python3 parsarium.py afl prepare zip cpp karchive runs/zip-karchive-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
