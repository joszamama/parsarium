# Container harness collection

Projects are organized as `projects/<format>/<ecosystem>/<package>/`. Each
project has a `manifest.json`, a Dockerfile, a byte-input harness, a valid-control
replay, and a recorded `verification.json`. The manifest links back to the
existing parser evidence and control. The third-party catalog remains
authoritative for package eligibility, release, and expected output; standard
API projects link to the separate official-documentation inventory.

The harness interface must accept the supplied bytes, call the package's real
local parser API, and consume an observable format-specific result. For C and
C++, the engine entry is `LLVMFuzzerTestOneInput`; the valid-control replay uses
the same parser function. The package source and harness are instrumented in
the container. A project is counted as containerized only after the valid
control passes and the coverage report shows executed lines in the package
source, not just in the harness. Shared underlying parser families remain
identified in the catalog.

The first batch is `png/c/libpng`, `png/c/stb`, `png/cpp/lodepng`, `png/python/pypng`,
`png/go/imaging`, `png/rust/png`, `png/java/pngj`, `png/javascript/pngjs`,
`png/php/marc1706_fast_image_size`, and `zip/c/libzip`. The next batch adds
`pdf/python/pypdf` and `pdf/python/pdfrw`, both with byte-input Atheris targets
and package line coverage during valid-control replay. The PDF reader source
file must show executed lines for each receipt. `http11/python/h11` adds raw
HTTP/1.1 request parsing and coverage in h11's request reader.

The next six projects cover the remaining formats: `mp3_id3v2/python/mutagen`,
`ascii_ply/python/plyfile`, `mp4/python/mutagen`, `wav/python/mutagen`,
`svg/python/svgelements`, and `ascii_pnm/python/netpbmfile`. The three Mutagen
projects exercise separate MP3/ID3v2, MP4, and WAVE parser modules from the
same pinned release; they are separate format paths, not independent packages.
The PLY and PNM projects pin their NumPy dependency wheel as well as the parser
wheel. All ten formats now have at least one covered container project.

`wav/python/stdlib_wave` is the first standard-library project. It pins the
CPython 3.13.1 image by architecture-specific digest and checks the SHA-256 of
its `wave.py` source before installing a pinned Atheris wheel. The valid-control
replay counts lines in CPython's `wave.py`, and the audit keeps this API separate
from third-party package paths.

The ZIP batch adds `zip/python/fsspec`, `zip/javascript/fflate`, and
`zip/go/klauspost_compress_zip`. Each reads the same valid ZIP control through
the package's documented byte or stream API. The Python receipt also records
delegation to CPython `zipfile`; the Go and JavaScript receipts require executed
lines in their package source. `data/projects-coverage.json` reports how many
format/ecosystem cells have at least one verified third-party project.

Each Dockerfile pins its base image by digest and its parser
source by SHA-256. Native C entries use libFuzzer and LLVM source coverage;
the C++ entry uses the LodePNG byte decoder with the same instrumentation.
PyPNG uses Atheris and Python line tracing of its pure-Python package. The Go
entry uses a compiled native Go fuzz test and Go's `-coverpkg` instrumentation.
Its valid-control profile records both the `imaging` wrapper and the delegated
`image/png` parser separately. The Go runtime image contains only two static
binaries. The Rust entry uses LLVM source coverage for the pinned `png` crate
and sanitizer coverage counters in its libFuzzer binary. The JavaScript entry
uses V8 source-range coverage for `pngjs` and Jazzer.js with explicit package
instrumentation. Its Node runtime uses a base with the glibc version required
by Jazzer's pinned native addon. V8 line counts are derived from executed
source ranges and can include import-time code; the receipt separately requires
execution in `parser.js`. The PHP entry uses a local temporary file for the
package's path API, Xdebug line coverage in the package, and a pinned
coverage-guided PHP fuzzer. Its receipt requires executed lines in `TypePng.php`.
The Java entry uses a pinned PNGJ JAR and source JAR, JaCoCo coverage in the
library bytecode, and Jazzer for the fuzz entry. Jazzer requires the JDK
attach module, so its runtime image carries a pinned JDK rather than a JRE.
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
python3 scripts/run_project.py png cpp lodepng
python3 scripts/run_project.py png python pypng
python3 scripts/run_project.py png go imaging
python3 scripts/run_project.py png rust png
python3 scripts/run_project.py png java pngj
python3 scripts/run_project.py png javascript pngjs
python3 scripts/run_project.py png php marc1706_fast_image_size
python3 scripts/run_project.py zip c libzip
python3 scripts/run_project.py pdf python pypdf
python3 scripts/run_project.py pdf python pdfrw
python3 scripts/run_project.py http11 python h11
python3 scripts/run_project.py mp3_id3v2 python mutagen
python3 scripts/run_project.py ascii_ply python plyfile
python3 scripts/run_project.py mp4 python mutagen
python3 scripts/run_project.py wav python mutagen
python3 scripts/run_project.py svg python svgelements
python3 scripts/run_project.py ascii_pnm python netpbmfile
python3 scripts/run_project.py wav python stdlib_wave
python3 scripts/run_project.py zip python fsspec
python3 scripts/run_project.py zip javascript fflate
python3 scripts/run_project.py zip go klauspost_compress_zip
python3 scripts/run_project_batch.py --format pdf --ecosystem python --dry-run
python3 scripts/run_project_batch.py --format pdf --ecosystem python
python3 scripts/run_project_batch.py --format zip --ecosystem go
python3 scripts/audit_projects.py --write
python3 scripts/audit_projects.py --check
```

The batch runner verifies selected projects sequentially and refreshes the
matrix audit only when every selected project passes. The audit compares
project manifests and successful coverage receipts against all third-party
parser paths in `data/*/*/parsers.json`. Standard-library and runtime-bundled
APIs are inventoried separately in `data/*/*/standard.json`; the audit records
their 45 paths and separate container progress. Pending third-party paths remain
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
