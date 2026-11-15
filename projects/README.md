# Container harness collection

Projects are organized as `projects/<format>/<ecosystem>/<package>/`. Each
project has a `manifest.json`, a Dockerfile, a byte-input harness, a valid-control
replay, and a recorded `verification.json`. The manifest links back to the
existing parser evidence and control. The catalog remains authoritative for
package eligibility, release, and expected output.

The harness interface must accept the supplied bytes, call the package's real
local parser API, and consume an observable format-specific result. For C and
C++, the engine entry is `LLVMFuzzerTestOneInput`; the valid-control replay uses
the same parser function. The package source and harness are instrumented in
the container. A project is counted as containerized only after the valid
control passes and the coverage report shows executed lines in the package
source, not just in the harness. Shared underlying parser families remain
identified in the catalog.

The first batch is `png/c/libpng`, `png/c/stb`, `png/python/pypng`,
`png/go/imaging`, `png/rust/png`, and `zip/c/libzip`. Each Dockerfile pins its base image by digest and its parser
source by SHA-256. Native C entries use libFuzzer and LLVM source coverage;
PyPNG uses Atheris and Python line tracing of its pure-Python package. The Go
entry uses a compiled native Go fuzz test and Go's `-coverpkg` instrumentation.
Its valid-control profile records both the `imaging` wrapper and the delegated
`image/png` parser separately. The Go runtime image contains only two static
binaries. The Rust entry uses LLVM source coverage for the pinned `png` crate
and sanitizer coverage counters in its libFuzzer binary.
The native final images contain the binaries, parser source for coverage display,
and LLVM coverage tools. The PyPNG image contains only pinned wheels and Python.
The runner disables
network access, mounts the control read-only, drops capabilities, and writes
profiles to an ignored `target/coverage` directory. It checks that the fuzz
engine starts in help mode and executes only the valid
control. No fuzz campaign or malformed-input experiment is run by this command.

Run from the repository root:

```sh
python3 scripts/run_project.py png c libpng
python3 scripts/run_project.py png c stb
python3 scripts/run_project.py png python pypng
python3 scripts/run_project.py png go imaging
python3 scripts/run_project.py png rust png
python3 scripts/run_project.py zip c libzip
python3 scripts/audit_projects.py --write
python3 scripts/audit_projects.py --check
```

The audit compares project manifests and successful coverage receipts against
all third-party parser paths in `data/*/*/parsers.json`. Pending paths remain
visible in `data/projects-coverage.json`; a copied Dockerfile or name alone
does not count. Ubuntu package repositories are not snapshot-pinned in the
pilot, so a later rebuild may use newer compiler and dependency package
revisions. The build receipt records the observed versions; pinning those
repositories is required before claiming bit-for-bit image reproducibility.

The same acceptance rule applies across ecosystems. Native targets use LLVM
source coverage in the parser build. Go targets need package coverage from an
instrumented Go build; Java targets need class coverage from the parser JAR;
JavaScript targets need V8 coverage for parser files; Python targets need
coverage of imported package code; PHP targets need PHP line coverage for the
package. Each project must select a suitable byte-input entry and record its
underlying native engine when a wrapper delegates parsing.
