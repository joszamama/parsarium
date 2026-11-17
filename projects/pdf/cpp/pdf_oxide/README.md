# pdf_oxide — PDF / C++

Pinned release: `0.3.78`. [Manifest](manifest.json) · [control receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/pdf/cpp/pdf_oxide/verification.json)

[API, control result, and parser family](../../../../catalog/pdf/cpp/pdf-oxide/README.md)

The harness passes input bytes to `pdf_oxide::Document::open_from_bytes` in the tagged C++17 header and prints `page_count()`. `libpdf_oxide.so` is built from the SHA-256-pinned v0.3.78 tag archive with its own `Cargo.lock` on Rust 1.92.0. The publisher binary is not used. Expected results:

| Input | Output |
| --- | --- |
| `controls/pdf/one-page.pdf` (control) | `{"pages":1}` |
| `two-page.pdf` (copy of `controls/pdf/two-page.pdf`) | `{"pages":2}` |
| `fuzzing/afl-native/pdf/cpp/pdf_oxide/valid-objstm.pdf` (AFL++ variant) | `{"pages":3}` |

`run-control.sh` also requires that both controls take the regular xref path, without reconstruction. It requires covered lines in `src/lexer.rs`, `src/parser.rs`, and `src/xref.rs`.

The valid control covers 871 source lines in the Rust engine, including 116 lexer, 47 parser, and 218 xref lines. The AFL++ build records 1,679 crate-scoped edges with 99.76% repeat-map stability; the three-page object-stream PDF adds 647 stable edges.

## Run from the repository root

```sh
python3 parsarium.py build pdf cpp pdf_oxide
python3 parsarium.py run pdf cpp pdf_oxide controls/pdf/one-page.pdf
python3 parsarium.py replay pdf cpp pdf_oxide CORPUS_DIR runs/pdf-pdf_oxide-cpp-replay
python3 parsarium.py afl build pdf cpp pdf_oxide
python3 parsarium.py afl prepare pdf cpp pdf_oxide runs/pdf-pdf_oxide-cpp-afl
python3 parsarium.py afl run runs/pdf-pdf_oxide-cpp-afl --check
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** AFL++ pcguard guards cover the whole `pdf_oxide` crate, not only its syntax modules. Stable rustc's `sancov-module` pass takes no source allowlist. Dependency crates and the C++ harness carry no guards. The AFL++ target is one-shot `/work/replay @@`.

**Shared parser:** This is the same Rust engine as [`projects/pdf/rust/pdf_oxide`](../../rust/pdf_oxide/README.md), reached through the C ABI. It is not an independent parser.
