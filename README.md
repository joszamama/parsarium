# Parsarium

Parsarium is a reproducible catalogue of libraries and bundled APIs that parse
specific formats. It currently contains verified C × PNG, WAV, and HTTP/1.1 batches,
verified C × ZIP and ASCII PNM batches, verified C++ × PNG, ZIP, and WAV batches,
and verified C++ × ASCII PNM, HTTP/1.1, and PDF batches, plus below-target
C and C++ × SVG and MP3 with ID3v2 batches,
a verified JavaScript × PNG pilot,
JavaScript × ZIP, MP4, WAV, PDF, SVG, HTTP/1.1, MP3 with ID3v2, ASCII PLY, and ASCII PNM,
plus a below-target JavaScript × Matrix Market search,
Go × ZIP, PNG, WAV, HTTP/1.1, MP4, MP3 with ID3v2, PDF, SVG, ASCII PLY, and ASCII PNM,
plus a below-target Go × Matrix Market search,
Python × PNG, ASCII PLY, ASCII PNM, ZIP, WAV, PDF, MP3 with ID3v2, MP4, HTTP/1.1, and SVG,
Python × Matrix Market, Rust × PNG, ZIP, MP4, WAV, PDF, SVG, HTTP/1.1, ASCII PLY,
ASCII PNM, Matrix Market, and MP3 with ID3v2, plus Java × ZIP, PNG, PDF,
WAV, MP4, HTTP/1.1, MP3 with ID3v2, SVG, and ASCII PNM, plus
an explicit 88-cell work matrix.
PHP × ZIP, PHP × PNG, PHP × ASCII PNM, and PHP × MP3 with ID3v2 have verified
20-parser batches, including PHP × WAV, PHP × PDF, and PHP × MP4. PHP × HTTP/1.1
and PHP × SVG each have a verified 20-path batch.
There are 71 cells at the 20-parser target, seven started below target, and 10
marked `not_started`;
a zero in those cells does **not** mean no parser exists. See the
[selection protocol](PROTOCOL.md) before adding a package.

## Reproduce the verified cells

The recorded runs used macOS arm64 and Python 3.10–3.14 by cell, plus Node.js 26.10.0, npm 11.19.1,
and Chromium 153.0.8010.12 through Playwright 1.63.0. The npm lockfile pins
all packages and integrity hashes. From the repository root:

```sh
python3 scripts/verify_c_png.py
python3 scripts/verify_c_http11.py
python3 scripts/verify_cpp_png.py
python3 scripts/verify_cpp_http11.py
python3 scripts/verify_c_pdf.py
python3 scripts/verify_cpp_pdf.py
python3 scripts/verify_c_svg.py
python3 scripts/verify_cpp_svg.py
python3 scripts/verify_c_mp3_id3v2.py
python3 scripts/verify_cpp_mp3_id3v2.py
python3 scripts/verify_c_ascii_pnm.py
python3 scripts/verify_cpp_ascii_pnm.py
python3 scripts/verify_c_zip.py
python3 scripts/verify_c_wav.py
python3 scripts/verify_cpp_zip.py
python3 scripts/verify_cpp_wav.py
python3 scripts/verify_php_zip.py
python3 scripts/verify_php_png.py
python3 scripts/verify_php_ascii_pnm.py
python3 scripts/verify_php_mp3_id3v2.py
python3 scripts/verify_php_wav.py
python3 scripts/verify_php_pdf.py
python3 scripts/verify_php_mp4.py
python3 scripts/verify_php_http11.py
python3 scripts/verify_php_svg.py
npm ci
npx playwright install chromium
npm run pilot:control
npm run pilot:verify
npm run zip:control
npm run zip:verify
npm run mp4:control
npm run mp4:verify
npm run mp3_id3v2:control
npm run mp3_id3v2:verify
npm run wav:control
npm run wav:verify
npm run pdf:control
npm run pdf:verify
npm run svg:control
npm run svg:verify
npm run http11:control
npm run http11:verify
npm run ascii_pnm:control
npm run ascii_pnm:verify
npm run ascii_ply:verify
npm run matrix_market:verify
python3 scripts/verify_go_zip.py
python3 scripts/verify_go_png.py
python3 scripts/verify_go_wav.py
python3 scripts/verify_go_http11.py
python3 scripts/verify_go_mp4.py
python3 scripts/verify_go_mp3_id3v2.py
python3 scripts/verify_go_pdf.py
python3 scripts/verify_go_svg.py
brew install assimp
python3 scripts/verify_go_ascii_ply.py
python3 scripts/verify_go_matrix_market.py
python3 controls/ascii_pnm/make_control.py
python3 scripts/verify_go_ascii_pnm.py
uv venv --python python3.13 adapters/python/png/.venv
uv pip sync adapters/python/png/requirements.lock --python adapters/python/png/.venv/bin/python --require-hashes
python3 scripts/verify_python_png.py
uv venv --python python3.12 adapters/python/ascii_ply/.venv
CMAKE_POLICY_VERSION_MINIMUM=3.5 uv pip sync adapters/python/ascii_ply/requirements.lock --python adapters/python/ascii_ply/.venv/bin/python --require-hashes
python3 scripts/verify_python_ascii_ply.py
uv venv --python python3.13 adapters/python/ascii_pnm/.venv
uv pip sync adapters/python/ascii_pnm/requirements.lock --python adapters/python/ascii_pnm/.venv/bin/python --require-hashes
python3 scripts/verify_python_ascii_pnm.py
uv venv --python python3.13 adapters/python/zip/.venv
uv pip sync adapters/python/zip/requirements.lock --python adapters/python/zip/.venv/bin/python --require-hashes
adapters/python/zip/.venv/bin/python controls/zip/make_zstd_control.py
python3 controls/zip/make_module_control.py
python3 scripts/verify_python_zip.py
uv venv --python python3.13 adapters/python/wav/.venv
uv pip sync adapters/python/wav/requirements.lock --python adapters/python/wav/.venv/bin/python --require-hashes
python3 scripts/verify_python_wav.py
uv venv --python python3.13 adapters/python/pdf/.venv
uv pip sync adapters/python/pdf/requirements.lock --python adapters/python/pdf/.venv/bin/python --require-hashes
uv venv --python python3.13 adapters/python/pdf/.venv_pdfx
uv pip sync adapters/python/pdf/requirements-pdfx.lock --python adapters/python/pdf/.venv_pdfx/bin/python --require-hashes
uv venv --python python3.13 adapters/python/pdf/.venv_slate
uv pip sync adapters/python/pdf/requirements-slate3k.lock --python adapters/python/pdf/.venv_slate/bin/python --require-hashes
python3 scripts/verify_python_pdf.py
uv venv --python python3.13 adapters/python/mp3_id3v2/.venv
uv pip sync adapters/python/mp3_id3v2/requirements.lock --python adapters/python/mp3_id3v2/.venv/bin/python --require-hashes
python3 scripts/verify_python_mp3_id3v2.py
uv venv --python python3.13 adapters/python/mp4/.venv
uv pip sync adapters/python/mp4/requirements.lock --python adapters/python/mp4/.venv/bin/python --require-hashes
python3 scripts/verify_python_mp4.py
uv venv --python python3.13 adapters/python/http11/.venv
uv pip sync adapters/python/http11/requirements.lock --python adapters/python/http11/.venv/bin/python --require-hashes
uv venv --python python3.10 adapters/python/http11/.venv310
uv pip sync adapters/python/http11/requirements-py310.lock --python adapters/python/http11/.venv310/bin/python --require-hashes
python3 scripts/verify_python_http11.py
uv venv --python python3.13 adapters/python/svg/.venv
uv pip sync adapters/python/svg/requirements.lock --python adapters/python/svg/.venv/bin/python --require-hashes
python3 controls/svg/make_control.py
python3 scripts/verify_python_svg.py
uv venv --python python3.13 adapters/python/matrix_market/.venv
CXXFLAGS='-include functional' uv pip sync adapters/python/matrix_market/requirements.lock --python adapters/python/matrix_market/.venv/bin/python --require-hashes
uv venv --python python3.10 adapters/python/matrix_market/.venv310
uv pip sync adapters/python/matrix_market/requirements-py310.lock --python adapters/python/matrix_market/.venv310/bin/python --require-hashes
python3 controls/matrix_market/make_control.py
python3 scripts/verify_python_matrix_market.py
python3 scripts/verify_rust_png.py
python3 scripts/verify_rust_zip.py
python3 scripts/verify_rust_mp4.py
python3 scripts/verify_rust_wav.py
python3 scripts/verify_rust_pdf.py
python3 scripts/verify_rust_svg.py
python3 scripts/verify_rust_http11.py
python3 scripts/verify_rust_ascii_ply.py
python3 scripts/verify_rust_ascii_pnm.py
python3 scripts/verify_rust_matrix_market.py
python3 scripts/verify_rust_mp3_id3v2.py
python3 scripts/verify_java_zip.py
python3 scripts/verify_java_png.py
python3 scripts/verify_java_svg.py
python3 scripts/verify_java_pdf.py
python3 scripts/verify_java_http11.py
python3 scripts/verify_java_mp3_id3v2.py
python3 controls/wav/make_control.py
python3 scripts/verify_java_wav.py
python3 scripts/build_matrix.py
python3 scripts/build_rankings.py
python3 scripts/validate_catalog.py
```

The C × PNG verifier uses `cc`, CMake, `pkg-config`, and zlib development headers. It downloads six source archives pinned by SHA-256 and checks fourteen locally installed C libraries pinned by exact release and binary SHA-256. The recorded result is **20/20 third-party package paths passing** on the valid 2×1 PNG control, with six paths unranked for lack of a comparable primary GitHub repository metric. The count does not imply twenty independent decoder engines or a complete most-used top twenty. Two plausible leads remain unresolved. Install the exact recorded library releases in [`source-lock.json`](data/c/png/source-lock.json) before rerunning; a later Homebrew revision will fail the binary check. See [`cell.json`](data/c/png/cell.json) for search limits and uncertainty. The ISO C standard library has no documented PNG parser; generic `stdio.h` input does not count.

The C++ × PNG verifier recompiles format-aware call sites as C++17 against the
same 20 pinned library releases, after rerunning the C source and binary checks.
It also checks an exact-release, binary-hashed SFML library. The observed result
is **21/21 package paths passing** the valid PNG control. Twenty paths share
releases and parser implementations with C; SFML provides a native C++ API but
bundles stb_image. Six plausible C++ leads, including OpenCV, OpenImageIO, and
Qt, remain unverified, so the [C++ PNG cell](data/cpp/png/cell.json)
does not claim a complete most-used top 20. The ISO C++ standard library has no
documented PNG parser.

The C++ × HTTP/1.1 batch verifies **20/20 package paths** against saved valid
request or response controls. Boost.Beast 1.92.0 and Poco.Net 1.15.4 are native
C++ APIs; eighteen C parser packages are called directly from C++17 and share
their releases and underlying engines with the C HTTP/1.1 cell. The verifier
checks SHA-256-pinned source archives, exact local library and header hashes,
and builds source releases where needed. Eight leads remain unresolved, so the
20-path count does not establish a complete most-used top 20. The ISO C++
standard library documents no HTTP parser. See the
[cell record](data/cpp/http11/cell.json) for search limits and uncertainty.

The C × PDF batch verifies **12/20 third-party package paths** from C call sites:
Poppler GLib, qpdf's C API, MuPDF, Ghostscript, PDFio, PDFium, Vanilla.PDF,
tspdf, ImageMagick, GraphicsMagick, libvips, and pdf_oxide. All return one parsed page from the
valid local control. qpdf requires a C++ linker for its C interface; PDFio
builds from pinned source. PDFium and Vanilla.PDF use
hash-pinned binary distributions with source-matched public headers. Apple Core
Graphics is independently verified as a macOS platform runtime API and is kept
outside the third-party ranking. See the
[C PDF cell record](data/c/pdf/cell.json) for search limits and uncertainty.

The C++ × PDF batch currently verifies **20/20 package paths**:
Poppler's C++ frontend, PoDoFo, qpdf, MuPDF, Ghostscript, PDFio, PDFium,
PDF-Writer, PDF4QT, Qt PDF, Xpdf, pdfmm, Docling Parse, Vanilla.PDF, tspdf,
Aspose.PDF FOSS, ImageMagick, GraphicsMagick, libvips, and pdf_oxide.
MuPDF, Ghostscript, PDFio, PDFium, Vanilla.PDF, and tspdf use C APIs called
directly from C++17; PDF-Writer and PDF4QT use native C++ parsers. All return one parsed page
from the valid PDF control. Release sources, installed headers, and libraries are
SHA-256 checked; PDFio, PDF-Writer, and PDF4QT are source-built. PDFium and
Vanilla.PDF use pinned binary distributions with public headers matched to
their source releases. PDF4QT uses a pinned Blend2D dependency and a recorded macOS core-only
source patch. Qt PDF's native QPdfDocument API shares the PDFium engine. Xpdf
links source-built object libraries and has no installed public library ABI.
Pdfmm is a source-built fork of PoDoFo. Docling Parse uses a bundled qpdf
engine; both shared lineages are recorded. tspdf is a source-built C11 reader
used from both ecosystems; its observed GitHub stars were zero, so external
adoption is unestablished. Aspose.PDF FOSS is source-built with a recorded
standard-header compatibility patch and had two observed stars. ImageMagick
and GraphicsMagick render PDF through their pinned Ghostscript delegate. libvips
loads PDF through its pinned Poppler module. pdf_oxide supplies a C ABI and a C++
RAII header over one Rust PDF engine; its publisher binary and source are pinned
separately, and source-to-binary equivalence is unestablished. One
lead remains unresolved. See the
[PDF cell record](data/cpp/pdf/cell.json) for search limits and uncertainty.

The C × SVG batch verifies **12/20 paths** and C++ × SVG verifies **15/20**.
librsvg, libvips, ImageMagick, GraphicsMagick, resvg, and PlutoSVG read the
local 2×1 SVG and render the expected red and green pixels in both ecosystems;
LunaSVG and QtSvg do so through their C++ document APIs. The pinned libvips build links librsvg;
ImageMagick uses its internal MSVG coder and GraphicsMagick uses its separate
SVG coder, both over system libxml2. resvg is source-built from a pinned
Cargo lock and supplies a separate Rust SVG engine. PlutoSVG and LunaSVG
have separate document parsers over the same PlutoVG rasterizer. Libsvgtiny
returns two shapes and their colors through its SVG Tiny parser; libsvg returns
parsed root dimensions, and libsvg-cairo renders pixels using that same libsvg
parser. ThorVG's C binding and C++ API both load and parse SVG dimensions
through its native SVG engine. SDL3_image reads the SVG through its embedded
NanoSVG parser; GdkPixbuf reads it through the pinned librsvg loader plugin.
QtBase QImageReader reads it through the same QtSvg plugin used by QtSvg.
All recorded SVG leads in these cells are resolved, while additional
projects outside the bounded Homebrew search remain uncertain; see the [C](data/c/svg/cell.json) and
[C++](data/cpp/svg/cell.json) records for search limits and uncertainty.

The C × MP3 with ID3v2 batch verifies **14/20 package paths** and the C++ batch verifies **15/20** on
the valid tagged MP3 control: TagLib, mpg123, FFmpeg libavformat, libid3tag,
id3lib, libsndfile, MediaInfoLib, SDL_mixer, SoX, libmad, miniaudio, CSFML, GStreamer, and libmpv. C++ also verifies native SFML.
The adapters return a parsed title, audio stream, or ID3v2 frame data. C and
C++ call sites share each package's engine; TagLib and id3lib C bindings use
their C++ cores. libsndfile shares mpg123 for audio and ID3v2 parsing. MediaInfoLib uses its native MPEG audio and ID3v2 parsers. SDL_mixer uses its own ID3v2 tag reader with an mpg123 audio backend. Its SDL3 major release was checked and excluded as the same upstream package. SoX parses audio from the tagged MP3 through libmad but does not expose its ID3v2 title. The direct libmad adapter skips the valid tag and decodes a frame, sharing the same audio engine as SoX. miniaudio decodes the tagged MP3 with bundled dr_mp3 code but does not expose tag text. CSFML and SFML use a shared minimp3 based decoder; both decode the tagged control but do not expose its title. GStreamer returns the ID3v2 title and MPEG audio stream fields using pinned demux and parser plugins. libmpv returns the tag title and MP3 track codec through its linked FFmpeg backend. The
source archives, native libraries, and
relevant dependencies are SHA-256 pinned; libid3tag's generated public header
is recorded separately from its source template. Homebrew's
install-on-request 365-day count ranks these packages within each cell, while
two leads remain unresolved. The separate C and C++ standard-library
inventories found no documented MP3 or ID3v2 parser. See the
[C](data/c/mp3_id3v2/cell.json) and [C++](data/cpp/mp3_id3v2/cell.json) records.

The C and C++ × ASCII PNM verifiers use valid 2×1 P3 red/green controls.
The C batch now has **20/20 verified package paths**: fourteen prior readers plus
JasPer 4.2.9, libimago 2.4.2, GEGL 0.4.72, SAIL 1.3.1, libpnmio, and IM
Toolkit 3.15. The verifier checks exact release source hashes or installed
library and plugin hashes, builds four additions from pinned source, then
checks dimensions and both decoded pixels. IM Toolkit exposes a C API backed
by C++ implementation code. libpnmio's README calls its tested source 1.2.7
while its VERSION file remains 1.2.6; the exact commit and source hash fix
what was tested, and the release-label conflict is recorded. Netpbm uses
official Subversion revision 5358 identifying release 11.02.30.

The C++ batch remains **20/20**, with fourteen call sites over C libraries and
six native C++ readers: CImg, Boost.GIL, wxWidgets, QtBase, pnm++, and
OpenImageIO. Its verifier reruns the full C batch before its own adapters.
CImg needs maxval on the dimensions line for the passing control; the other
valid P3 layout is recorded as a limitation. SDL2_image and SDL3_image share
one decoder lineage, and libpnmrw and Netpbm share PBMPLUS ancestry. The C
search recorded six bounded Conan recipe-name hits and targeted documentation
leads; licensing for libpixmap and a named PPMA_IO release remain unresolved.
Twenty verified paths do not establish a definitive most-used top 20. Ten C
paths and eight C++ paths lack comparable primary GitHub stars and remain
unranked. Only ASCII P3 is established for every path. Neither scoped
standard library documents a PNM-aware parser.

The [C × HTTP/1.1 cell](data/c/http11/cell.json) contains **20/20 verified
package paths**: llhttp, Node http-parser, PicoHTTPParser, Mongoose, httpp,
HTTPParserC, GNU libmicrohttpd, libevhtp, LibHTP, libwebsockets, libonion,
libsoup, Apache Serf, facil.io C STL 0.8, facil.io 0.7, libhv, libparsehttp,
H2O, finwo/http-parser.c, and Samsung http-parser. Eighteen parsed
the method, request path or target, and version of a valid local GET request after complete
header parsing. `python3 scripts/verify_c_http11.py` checks SHA-256 source
archives, the exact local llhttp 9.4.3 and libmicrohttpd 1.0.10 libraries and
headers, plus the libwebsockets 5.0.0_2 and libsoup 3.8.1 libraries and headers, rebuilds all twenty
adapters, and replays the controls. libwebsockets yielded the parsed method,
target and Host header from an adopted local read buffer. LibHTP 0.5.53
is rebuilt from its pinned source with Autotools and zlib. libonion 0.8 is
rebuilt from pinned source with a recorded macOS compatibility step and
hash-checked libev 4.33; its local-byte API yielded method, path, version,
Host and query. libsoup's documented local-byte request-head API yielded method,
target, version and Host. Apache Serf's local response bucket yielded status,
reason, headers and body from a valid 200 response. Its source build excludes
an unrelated SSL bucket object that fails with the local OpenSSL headers. The libmicrohttpd
adapter supplies the request through a local socket stream. Four bounded Conan recipe-name queries saved
24 hits and 22 distinct names; project documentation supplied PicoHTTPParser,
Mongoose, httpp, HTTPParserC, libevhtp, LibHTP, libwebsockets, libonion, libsoup,
Apache Serf, both facil.io distributions, libhv, libparsehttp, H2O,
finwo/http-parser.c, and Samsung http-parser
outside those windows. HTTPParserC distributes llhttp C source and shares its
parser engine. libhv bundles a modified Node http-parser 2.9.1 engine; its
separate tagged library distribution is counted once and the shared family is
recorded. H2O bundles PicoHTTPParser as its HTTP/1 parser; its tagged H2O
distribution shares that parser family. Samsung's tagged fork shares the Node
http-parser family. The two facil.io packages have distinct tagged distributions and
input APIs but share parser lineage. libevhtp ships its own htparse scanner;
libparsehttp and finwo/http-parser.c use separate local-byte scanners. The
finwo stable tag is pinned by its exact commit and SHA-256, as are its four
build dependencies.
GitHub project stars rank seventeen paths only within C;
libmicrohttpd, libsoup and Apache Serf have no primary GitHub repositories and remain unranked.
The working count is met, while eight leads and searches outside the saved
Conan windows remain uncertain. The ISO C standard library provides
no documented HTTP/1.1 request parser.

The C × ZIP verifier uses `cc`, CMake, `make`, and `pkg-config` with eight locally installed
libraries pinned by exact release and binary SHA-256, plus eleven source-built
or source-integrated libraries pinned by archive or file SHA-256 in
[`source-lock.json`](data/c/zip/source-lock.json). SQLite Zipfile also links an
exact-release, binary-hashed SQLite library. The libc7zip build also pins
its official 7-Zip engine source by SHA-256 and currently uses the macOS arm64
build path. libtfs uses SHA-locked macOS arm64 release archives and a pinned
local OpenSSL archive; Tcl Zipfs uses binary-hashed Tcl 9.1.0 and libtommath
libraries (`brew install openssl@3 tcl-tk` on the recorded host; the verifier
rejects version or hash mismatches). AOSP libzipfile uses individually SHA-locked files from the Android
4.4.4_r2 release commit because the Gitiles tarball bytes vary across downloads.
All **20/20 third-party
package paths passed** on the same one-entry DEFLATE ZIP control used in the
other ecosystems. Nineteen returned entry name and decompressed bytes; zipc
returned decompressed bytes for a known named entry. The working goal of 20 is
met, while the most-used search remains incomplete. Fifteen paths have primary GitHub
repository star metrics; five remain unranked. MiniZip and minizip-ng share
parser lineage, kuba-zip bundles miniz, unzipLIB includes a modified MiniZip,
libc7zip wraps lib7zip and the 7-Zip engine, lowzip has its own ZIP reader,
Info-ZIP UnZip exposes a separate C API, JUnzip parses ZIP records with
zlib for DEFLATE, SQLite Zipfile parses ZIP records through a virtual table,
zipc reads known entries using zlib, libtfs exposes a C facade over libzip,
Tcl Zipfs parses ZIP in the Tcl runtime through its documented C API, and
AOSP libzipfile is a separate ZIP record reader built outside the Android runtime.
The 23 Conan recipe-name and 159 GitHub search hits (151 unique names in all)
are discovery results, not a most-used ranking; eleven leads remain unresolved.
The [C ZIP cell summary](data/c/zip/cell.json) records the search limits and
uncertainty. The ISO C standard library has no documented ZIP parser.

The C × WAV verifier builds pinned `dr_wav`, miniaudio, Audio File Library, and
native SDL2 sources. It also checks exact-release, binary-hashed libsndfile,
raylib, FFmpeg, SoX, SDL3, SDL3_mixer, aubio, CSFML, Allegro, SDL2_mixer,
FreeALUT, SDL2-compat, SDL2_sound, SDL3_sound, TagLib C bindings, and GStreamer.
All **20/20 third-party package paths passed** the valid four-sample PCM WAV
control. Eighteen returned parsed format values and four decoded samples;
SDL3_mixer returned format values and duration, while TagLib returned sample
rate, channels, and bitrate. The working count is reached, while the most-used
search remains incomplete. The [C WAV cell](data/c/wav/cell.json) records the
bounded Conan Center recipe search, one unresolved lead, and shared `dr_wav`
and SDL lineage, including the shared SDL_sound upstream for both major-version
packages. Its [ranking](data/c/wav/ranking.md) uses only primary
GitHub repository stars within C; SoX and GStreamer remain unranked. The ISO C standard
library has no WAV parser. The Audio File Library source build applies a
documented compatibility patch for a signed-shift constant expression.

The C++ × ZIP verifier runs the C ZIP pin and control checks, then builds
C++ call sites for a selected seventeen C packages and ten pinned C++ libraries. All
**27/27 package paths passed** the valid archive control. Twenty-six returned
entry name and decompressed contents; zipc returned known-entry content.
libzippp wraps the verified libzip release,
Troldal Zippy bundles miniz, Zipper and QuaZip wrap classic MiniZip, bit7z
and libc7zip use pinned 7-Zip engines through separate APIs, QArchive wraps
libarchive, and the separate
Sebastian Zipper package and unzipLIB also share classic MiniZip lineage;
Info-ZIP UnZip uses its separate engine; JUnzip, SQLite Zipfile and zipc reuse
their pinned C releases. These paths are not twenty-seven
independent ZIP engines. Six plausible C++ leads remain
unresolved, so the [C++ ZIP cell](data/cpp/zip/cell.json)
records that the numerical goal is met, while search remains incomplete and the
cell does not claim a definitive most-used top 20. The ISO C++
standard library has no documented ZIP parser.

The C++ × WAV verifier reruns the C WAV release and control checks, builds
twenty C++17 call sites for those exact packages, and checks pinned SFML 3.0.2
and header-only AudioFile 1.1.4 through native C++ APIs. All **22/22 package
paths passed** the valid four-sample PCM WAV control. SFML shares an underlying
engine with the separate CSFML package; the C++ AudioFile package is unrelated
to the C Audio File Library. The [C++ WAV cell](data/cpp/wav/cell.json) records
seven bounded Conan Center recipe-name searches, three unresolved leads,
and the exact release and binary hashes. Its [ranking](data/cpp/wav/ranking.md)
uses primary GitHub stars within C++; SoX and GStreamer remain unranked. The
numerical goal is met, while a definitive most-used top 20 remains unproven.
The ISO C++ standard library has no documented WAV parser.

The PHP × ZIP verifier installs twenty exact Composer package releases from six
lockfiles and runs local-file readers on the same one-entry DEFLATE control.
All **20/20 third-party paths and 2/2 bundled PHP APIs passed**. Fourteen package
paths use PHP ZipArchive/libzip; the [PHP ZIP ranking](data/php/zip/ranking.md)
labels shared families and uses Packagist lifetime downloads only to order the
verified third-party paths. PclZip uses a separate lock because UnifiedArchive
declares it as a Composer replacement; older Laravel and Symfony packages also
need separate dependency sets. Chumper’s documented entry-listing method fails
on PHP 8.5, but its named-entry read API passed and is ranked at that narrower
scope. Nonfatal PHP 8.5 warnings are captured in
[verification.json](data/php/zip/verification.json).
Three bounded Packagist searches recorded 300 hits, and three plausible leads
remain unresolved. See the [cell summary](data/php/zip/cell.json) for the
exact search limits and uncertainty. Reproduction requires PHP 8.5 with zip
and Phar extensions, plus Composer 2; the verifier installs locked packages.

The PHP × PNG verifier installs twenty exact Composer releases from two lockfiles.
All **20/20 third-party paths and 4/4 bundled PHP APIs passed** the valid 2×1
red/green PNG control. Eighteen paths share PHP GD decoding directly or through
Intervention Image and Imagine; FastImageSize reads PNG dimensions from headers
in PHP; php-vips uses installed libvips 8.18.7 through PHP FFI. The second lock
isolates ImageHash's Intervention Image 3 dependency from version 4 in the main
lock. The bundled API inventory keeps header dimension readers separate from
pixel decoders. Three Packagist searches saved 300 discovery hits. Six plausible
leads remain unresolved, and two aliases were rejected as duplicate source. The
[PHP PNG cell summary](data/php/png/cell.json) records the search limits and
uncertainty. Reproduction requires PHP 8.5 with GD and FFI, libvips 8.18.7,
and Composer 2.

The [PHP × ASCII PNM ranking](data/php/ascii_pnm/ranking.md) has twenty pinned
third-party paths passing the valid two-pixel P3 control. Six use libvips,
thirteen use ImageMagick (including a SHA-256-pinned PECL Imagick release),
and one uses FFmpeg. These are package paths across three decoder families.
Eight bounded Packagist searches saved 242 hits and 239 distinct names. Two
leads remain unresolved; the numerical working goal is met, while the bounded
search does not establish a definitive most-used top twenty.
The [runtime inventory](data/php/ascii_pnm/standard.json) records that the
tested PHP core and GD APIs did not parse the control. Reproduction requires
PHP 8.5 with FFI, libvips 8.18.7, ImageMagick 7, FFprobe, phpize, and Composer 2. The
verifier builds Imagick into ignored cache from the pinned PECL source archive.

The [PHP × MP3 with ID3v2 ranking](data/php/mp3_id3v2/ranking.md) has twenty
pinned package paths passing valid ID3v2.3 or ID3v2.4 tagged MP3 controls.
Wrappers and forks share getID3, Mp3Info, PHP Reader, MediaInfoLib, FFmpeg,
MetaAudio, or libsndfile parser families, as recorded per package. Nine bounded
Packagist searches saved 205 hits and 151 distinct names. Thirteen plausible
leads remain unresolved, so the verified ranking is not a definitive most-used
top twenty. The
[runtime inventory](data/php/mp3_id3v2/standard.json) records that PHP Fileinfo
returns only a MIME type; the separate PECL id3 extension was absent.
The MediaInfo path requires the `media-info` 26.10 Homebrew formula (or an
equivalent `mediainfo` CLI on `PATH`) and uses the committed 18-second control.
The Pyrex adapter switches MediaInfo 26.10 to its older XML output mode so the
pinned package can read it.

The [PHP × WAV ranking](data/php/wav/ranking.md) records twenty pinned
package paths passing valid mono PCM16 controls. Eleven adapters reuse the
exact Composer releases from the PHP MP3 cell; nine have isolated WAV locks.
Twelve bounded Packagist searches saved 595 hits and 437 distinct names.
Twelve relevant leads remain unresolved, so this is not a definitive most-used
top twenty. The family field distinguishes getID3, FFmpeg, MediaInfoLib,
libsndfile, SoX, and native PHP WAV readers. The four-second rhythmic control
supports the pinned BPM reader; its generator is `controls/wav/make_control.py`.
The [PHP WAV runtime inventory](data/php/wav/standard.json) records that
Fileinfo returns only a MIME type, while generic FFI and file I/O are not WAV
parsers. The WAV replay requires the PHP 8.5 extensions and MediaInfo/FFmpeg
CLI tools used by the PHP MP3 batch, plus SoX on `PATH`. Run
`python3 scripts/verify_php_wav.py` from the repository root.

The [PHP × PDF ranking](data/php/pdf/ranking.md) has twenty pinned package
paths passing the valid one-page PDF control. The six-query Packagist snapshot
saved 546 hits and 412 distinct names; two named leads remain unresolved.
Several wrappers share the FPDI or TCPDI parser family. Spatie and ottosmops
use Poppler `pdftotext` 26.11.0; Gufy uses Poppler `pdfinfo` and `pdftohtml`
26.11.0; mikehaertl/php-pdftk uses `pdftk-java` 3.3.3.
The [PHP PDF runtime inventory](data/php/pdf/standard.json) records MIME-only
Fileinfo and GD's failed PDF image reads. Run `python3 scripts/verify_php_pdf.py`
from the repository root. Set `PARSARIUM_PDFTK` to a working `pdftk-java`
executable if it is not at `/opt/homebrew/bin/pdftk`. Set
`PARSARIUM_PDFINFO` and `PARSARIUM_PDFTOHTML` if the Poppler executables
are not at their `/opt/homebrew/bin` paths. The pinned Jurosh release's
source LICENSE says Apache-2.0 while its Composer metadata says MIT; the
source license is recorded.

The [PHP × MP4 ranking](data/php/mp4/ranking.md) records 20 pinned package
paths passing the valid 2 × 2 H.264/AAC MP4 control. Twelve bounded
Packagist searches saved 495 hits and 387 distinct package names. These paths
share getID3, MediaInfoLib, and FFmpeg parser families, alongside a native PHP
MP4 atom reader; nine relevant leads remain unresolved. This is a verified
20-path collection, not a definitive most-used top 20. The
[PHP MP4 runtime inventory](data/php/mp4/standard.json) records MIME-only
Fileinfo and GD's failed reads. Run `python3 scripts/verify_php_mp4.py`
from the repository root.

The [PHP × HTTP/1.1 ranking](data/php/http11/ranking.md) records 20 pinned
package paths parsing the valid saved GET request, including its target,
protocol version, and headers. Eight bounded Packagist searches saved 441 hits
and 389 distinct names; four named leads remain unresolved. The
[runtime inventory](data/php/http11/standard.json) separately verifies the PHP
CLI built-in server on the same raw request bytes. ReactPHP and Amp were
verified through their documented local server APIs; other packages accepted
the saved bytes or a local stream directly. Guzzle PSR-7 forks, Guzzle 3 package
paths, Zend/Laminas HTTP, and Diactoros descendants share parser lineage, as
recorded in the [parser rows](data/php/http11/parsers.json). The collection
meets the 20-path target but is not a definitive most-used top 20. Run
`python3 scripts/verify_php_http11.py` from the repository root. Install
`php@8.4` and `php@8.2` from Homebrew plus `shivammathur/php/php@7.4` for
replaying packages pinned to those runtimes. The verifier uses their
`/opt/homebrew/opt` paths by default; override them with `PARSARIUM_PHP84`,
`PARSARIUM_PHP82`, and `PARSARIUM_PHP74`.

The [PHP × SVG ranking](data/php/svg/ranking.md) has 20 pinned, distinct source
releases that parsed the valid two-rectangle SVG control through typed document,
dimension, validator, sanitizer, optimizer, or rasterizer APIs. Eight bounded
Packagist searches saved 391 hits and 241 distinct names; six named leads remain
unresolved. Two registry aliases of identical source releases were excluded.
The [runtime inventory](data/php/svg/standard.json) separately verifies
`getimagesize()` and `getimagesizefromstring()` SVG dimensions in PHP 8.5 with
ext-libxml. The 20-path working goal is met; shared sanitizer, PHP-SVG, dompdf,
and librsvg families are recorded in the [parser rows](data/php/svg/parsers.json).
Run `python3 scripts/verify_php_svg.py` from the repository root with PHP 8.5,
PHP 7.4, Composer 2, Node/npm for sharp, rsvg-convert 2.63.4, and the pinned
PECL Imagick build script's ImageMagick toolchain. The verifier installs sharp
from the root npm lock when needed and builds Imagick from its source lock.

`pilot:control` generates the 71-byte PNG in `controls/png/red-green.png` with
SHA-256 `5a852fbaaaecaf4cd14c01e150c7f881c5c5894b0a1e3c53be7e007c58374ee6`.
It has two opaque pixels: red and green. The verifier runs each package adapter
against the path, checks parsed dimensions and either decoded pixels, parsed
chunks, or the format-bearing header result, then writes dated JSON results.
It also runs the browser-bundled `createImageBitmap(Blob)` adapter with the same
control. The observed pilot result is **21/21 third-party packages and 1/1
runtime API passing**. A fresh run replaces the dated result files.
It also generates `controls/png/red-green-title.png`, the same valid pixels
with a `Title=Parsarium` text chunk for metadata readers.

`zip:control` creates a deterministic 128-byte ZIP with one DEFLATE-compressed
`hello.txt` entry containing `parsarium\n` (SHA-256
`c534fa083d1da92474852ca9168ba0793740c25205f828915a1d862bd78c776b`).
The ZIP adapter checks both the parsed entry name and decompressed content.
The observed batch result is **21/21 third-party packages and 1/1 Node.js
built-in API passing**.

The Java × ZIP batch uses Maven 3.9.16 to compile for Java 21 and a SHA-256
lock for all 67 resolved JARs. `python3 scripts/verify_java_zip.py` rebuilds the
adapter, checks the locked classpath, and runs the same ZIP control through
20 documented Maven package paths plus five separate JDK 21 APIs. The recorded
result is **20/20 third-party paths and 5/5 JDK APIs passing**. Two of four
bounded Maven Central search queries timed out; the other two saved 115 hits,
including 100 of 178 mostly unrelated Java ZIP hits. Discovery and
higher-adoption lead review remain incomplete. Several package paths wrap shared
underlying parser families; see the
[Java ZIP ranking](data/java/zip/ranking.md), [cell summary](data/java/zip/cell.json),
and [unresolved leads](data/java/zip/leads.json). `snapshot_maven_zip.py`
refreshes registry and deps.dev evidence when needed; it is not part of the
offline reproduction command.

The Java × PNG batch uses Maven 3.9.16 and JDK 21 on macOS arm64. Its
SHA-256 lock covers 86 resolved JARs, including the native JavaFX and OpenCV
artifacts. `python3 scripts/verify_java_png.py` validates the PNG signature,
chunk CRCs, IHDR fields, and two decoded RGBA pixels independently, rebuilds
the adapter, checks all locked JAR and pinned release hashes, then runs the
20 third-party package paths and four separate JDK APIs. The recorded result
is **20/20 third-party paths and 4/4 JDK APIs passing**. Eight third-party
paths report both pixels; twelve report format-aware PNG dimensions. Five
bounded Maven Central searches saved 55 broad `png` hits; three timed out and
one returned zero. Targeted release lookups and documented APIs supplied the
verified candidates; broader discovery and higher-adoption lead review remain
uncertain. Several paths share underlying Java ImageIO, JCodec, or iText code.
See the [Java PNG ranking](data/java/png/ranking.md),
[cell summary](data/java/png/cell.json), and
[unresolved leads](data/java/png/leads.json). Run
`python3 scripts/snapshot_maven_png.py` only when refreshing registry and
deps.dev evidence.

The [Java × SVG ranking](data/java/svg/ranking.md) contains **20/20**
verified package paths: four Apache Batik artifacts, four EchoSVG artifacts,
JSVG, SVG Salamander, iText SVG, TwelveMonkeys ImageIO Batik, BWeng20
jSVGIcon, JairoSVG, imageio-native-vips, Apache FOP, Radiance, Aurora,
gsvg, and AndroidSvgTranscoder. All twenty passed the valid
2×1 red/green SVG control in
`python3 scripts/verify_java_svg.py`, which rebuilds the adapter and checks
the SHA-256 classpath locks for 97 main JARs, two JairoSVG JARs, two native
libvips wrapper JARs, and 32 EchoSVG JARs. The Batik and EchoSVG artifact
paths share families; four EchoSVG paths have no comparable deps.dev metric
and remain unranked. JairoSVG uses JDK 25; imageio-native-vips uses JDK 27
and host libvips 8.18.7. Set `PARSARIUM_JAVA27_HOME` if JDK 27 is not at
`/opt/homebrew/opt/openjdk`, and
set `PARSARIUM_JAVA25_HOME` if it is not at `/opt/homebrew/opt/openjdk@25`.
The [cell summary](data/java/svg/cell.json) records 112 bounded Maven
search hits, a broad-query timeout, and five unresolved leads. The scoped
[JDK 21 inventory](data/java/svg/standard.json) found no bundled SVG reader;
a bare-JDK ImageIO probe returned no SVG reader on the control. Run
`python3 scripts/snapshot_maven_svg.py` and `python3 scripts/enrich_java_svg.py`
only to refresh discovery and release/metric snapshots.

The [Java × ASCII PNM ranking](data/java/ascii_pnm/ranking.md) currently has
**20/20 verified package paths**: Apache Commons Imaging, TwelveMonkeys ImageIO,
JAI ImageIO, ImageJ, the OpenPnP OpenCV binding, Thumbnailator, BoofCV, and
Apache Tika, imageio-native-vips, imageio-native-magick, JavaCV, and Bytedeco
FFmpeg, Jaffree, bramp FFmpeg, the v47 Jaffree fork, Imagic FFmpeg Java,
JAVE2, the Lafa TwelveMonkeys fork, IJ Plugins ImageIO, and im4java.
Eleven paths returned both pixels of the valid ASCII P3 PPM control; Tika
reported dimensions, JavaCV decoded a frame, and seven FFmpeg or FFprobe paths
parsed the PPM format or codec and dimensions. These seven share FFmpeg's decoder.
`python3 scripts/verify_java_pnm.py` rebuilds the adapters, checks twenty Maven
releases, 90 locked classpath JARs, and host FFprobe and ImageMagick identify
executable hashes, then replays all twenty paths plus a
bare-JDK probe. The native paths require JDK 27 and the recorded host libvips
or ImageMagick release. The JDK 21 probe found no
bundled PNM reader. The [cell summary](data/java/ascii_pnm/cell.json) records
12 bounded registry hits, three timed-out queries, one unresolved lead, and
the remaining selection uncertainty. Refresh the discovery and release
snapshots only with `python3 scripts/snapshot_maven_pnm.py` and
`python3 scripts/enrich_java_pnm.py`.

The Java × PDF batch requires Maven 3.9+, JDK 25, and macOS arm64 for two
PDFium native bindings. Set `PARSARIUM_JAVA25_HOME` if JDK 25 is not at
`/opt/homebrew/opt/openjdk@25`. Its SHA-256 locks cover five isolated Maven
classpaths; the PDF Clown 0.1.2 Beta adapter downloads the official release
archive on first run and checks the archive and bundled JAR hashes. Run
`python3 scripts/verify_java_pdf.py` from the repository root. The recorded
result is **20/20 third-party package paths passing** on the valid one-page
control. Nineteen Maven paths have comparable deps.dev exact-version direct
dependent counts; the non-Maven PDF Clown release remains unranked. Two of five
bounded Maven searches timed out and 11 plausible leads remain unresolved, so
the current 20 are not a proven exhaustive top 20. No Java SE 25 PDF parser
API was documented in the separate runtime inventory. See the
[Java PDF ranking](data/java/pdf/ranking.md),
[cell summary](data/java/pdf/cell.json), and
[unresolved leads](data/java/pdf/leads.json). Run
`python3 scripts/snapshot_maven_pdf.py` only to refresh registry and deps.dev
evidence; it is not part of offline reproduction after the PDF Clown archive
has been cached.

The Java × MP4 batch uses Maven 3.9+, JDK 25, and macOS arm64 for
the pinned native FFmpeg bindings. Its fourteen module classpaths have 22, 3,
12, 3, 3, 7, 2, 5, 1, 2, 11, 1, 2, and 3 SHA-256-locked JARs. Run
`python3 controls/mp4/make_control.py` to restore the valid 2×2 H.264/AAC
control, then `python3 scripts/verify_java_mp4.py` from the repository root.
Set `PARSARIUM_JAVA25_HOME` if JDK 25 is elsewhere. The recorded result is
**20/20 third-party package paths passing**: MP4Parser's isoparser and muxer
artifacts, metadata-extractor, JCodec, Apache Tika's MP4 parser, JavaCV,
the Bytedeco FFmpeg binding, Jaffree, bramp FFmpeg, JAVE2, Imagic FFmpeg Java,
the v47 Jaffree fork, vlcj-info, the amilesend MediaInfo wrapper, JAAD,
Tianscar Java Sound AAC, Red5 IO, the older CoreMedia isoparser, Tallison
isoparser, and Liferay's patched MP4Parser. Five paths share the MP4Parser
family; Tika uses metadata-extractor and Red5 uses JCodec;
seven paths rely on FFmpeg or FFprobe; two use libmediainfo; the two JAAD
paths share a pure Java demultiplexer family. The original MP4 has optional
metadata that JAAD 0.8.7 cannot parse, so that path uses a second valid MP4
restored by `python3 controls/mp4/make_no_udta_control.py`. The amilesend
adapter uses a valid larger MP4 control generated by
`python3 controls/mp4/make_padded_control.py` because its API requires at
least 65,536 bytes. Red5 uses a valid three-second control restored by
`python3 controls/mp4/make_three_second_control.py`. Set
`PARSARIUM_FFPROBE_DIR` if the pinned FFprobe 9.0.2 binary is outside
`/opt/homebrew/bin`; set `PARSARIUM_LIBMEDIAINFO_DIR` if the pinned
libraries are outside `/opt/homebrew/lib`.
A JDK-only probe found no ImageIO or Java Sound reader for the control;
the separate official API inventory records no documented Java SE 25 MP4
parser. Nine bounded Maven searches saved 128 hits, 122 unique;
the broad mp4 query returned 100 of 350 hits and most appear unrelated to MP4
media. Three targeted documentation leads remain unresolved. This batch meets
the 20-path working count; the searches do not establish an exhaustive top 20.
See the [Java MP4 ranking](data/java/mp4/ranking.md),
[cell summary](data/java/mp4/cell.json), and [leads](data/java/mp4/leads.json).
`python3 scripts/snapshot_maven_mp4.py` refreshes Maven and deps.dev evidence.

The Java × WAV batch uses Maven 3.9+, JDK 25, and macOS arm64. Nine module
classpaths lock 57 regular, 5 Bytedeco, 3 Jaffree, 3 JAVE2, 12 Bramp,
3 Imagic, 7 v47 Jaffree, 2 vlcj-info, and 5 amilesend JARs by SHA-256.
FFprobe wrappers use a checksummed local FFprobe 9.0.2 executable; set
`PARSARIUM_FFPROBE_DIR` when it is outside `/opt/homebrew/bin`.
vlcj-info uses checksummed Homebrew libmediainfo 26.10 and libzen 0.4.41_1;
install them with `brew install libmediainfo` and verify that Homebrew resolves
the recorded versions before running the adapter.
Set `PARSARIUM_LIBMEDIAINFO_DIR` when they are outside `/opt/homebrew/lib`.
The amilesend binding uses its pinned macOS arm64 native JAR.
`python3 controls/wav/make_control.py` regenerates the valid 556-byte
256-frame mono PCM control (SHA-256
`d0dd329ac475ac10d5d918633c6dd798e4fc83db5f4c6afccfaa60e405d41ea7`)
and a valid 65,580-byte control for the amilesend file API, which requires at
least 65,536 bytes. Run `python3 scripts/verify_java_wav.py` from the repository
root; set `PARSARIUM_JAVA25_HOME` if JDK 25 is elsewhere.
The recorded result is **20/20 third-party package paths and 2/2 JDK APIs passing**.
The JDK adapter runs without a third-party classpath. Shared wavfile, Java Sound,
FFmpeg and libmediainfo families are labeled in the ranking. Five bounded Maven
queries saved five hits (three unique) across refreshes, and seven plausible
leads remain unresolved. TarsosDSP 2.5 is pinned from its official non-Central
repository and has no comparable deps.dev count. The collection meets the
20-path working goal but is not a proven exhaustive most-used top 20. See the
[Java WAV ranking](data/java/wav/ranking.md), [cell summary](data/java/wav/cell.json),
and [unresolved leads](data/java/wav/leads.json). Run
`python3 scripts/snapshot_maven_wav.py` to refresh Maven and deps.dev evidence.

The Java × HTTP/1.1 batch verifies **20/20 pinned Maven package paths** on
committed valid GET request and 200 response controls.
`python3 scripts/verify_java_http11.py` rebuilds the adapter and checks SHA-256
hashes for all 77 resolved JARs. Sixteen paths report request method, target,
and two headers; fifteen also expose the request version. The Sentinel response parser reports status line, status code, Content-Type, and body. JGlobus reports response status, reason, Content-Type, and Content-Length; java-warc reports status, Content-Type and body via an Apache HttpCore-based wrapper. Apache Commons HttpClient 3.1 reports version, status, reason, and headers from its own response-head parser.
Apache MINA and Grizzly supply separate native HTTP decoders. Apache HttpCore 4, its NIO artifact, and HttpCore 5 share an upstream family,
as do the Netty 3, 4, and 5 release lines; the
Netty 5 release is alpha. Jodd HTTP and RawHTTP parse the saved local stream
directly. NanoHTTPD's local stream session exposes parsed request fields through
a callback. jwarc, webarchive-commons, and JWAT expose direct parsers that read
the raw HTTP request without a WARC container. This cell meets the **20-path working goal**; the incomplete search does not prove a definitive most-used top 20. The bounded search saved two identical 100-hit broad windows out of
7,858 results, while three other queries timed out. One plausible lead, ActiveJ HTTP, remains unresolved; the historical WebPieces artifact is excluded as a duplicate parser line. See the
[Java HTTP/1.1 ranking](data/java/http11/ranking.md),
[cell summary](data/java/http11/cell.json), and
[JDK inventory](data/java/http11/standard.json). Run
`python3 scripts/snapshot_maven_http11.py` to refresh Maven and deps.dev evidence.

The Java × MP3 with ID3v2 batch verifies **20/20 pinned Maven package paths**.
Readers report ID3v2 text fields, MP3 frames or decoded samples, or both,
according to their documented APIs. The adapters use three valid tagged MP3
controls: a 1-second 8 kHz file, a 1-second 44.1 kHz file for JavaMP3, and a
72,941-byte 18-second file for the amilesend MediaInfo wrapper. JDK 25 is
required for the Java TagLib adaptation. Run
`python3 scripts/verify_java_mp3_id3v2.py` from the repository root to rebuild
the nine modules and check 67 SHA-256 locked JARs, the local FFprobe binary,
and libmediainfo/libzen. A JDK-only Java Sound probe rejects the 8 kHz control
and is recorded separately. Several paths share JLayer, FFmpeg, or MediaInfo
families. All five bounded Maven Central search queries timed out, and one
plausible lead remains unresolved, so these 20 paths are not a proven most-used
top 20. See the [Java MP3 ranking](data/java/mp3_id3v2/ranking.md) and
[cell summary](data/java/mp3_id3v2/cell.json).

`mp4:control` restores a fixed 2670-byte MP4 with one 2×2 H.264 video frame,
one second of silent 8 kHz AAC audio, title `Parsarium`, and creation time
`2020-01-02T03:04:05Z` (SHA-256
`10086c39c7226726579924794cd7c0bbafe65de38021bd0f38f6da9d23d24643`).
The source bytes are committed as base64, so FFmpeg is not needed to reproduce
the control. Package adapters check parsed boxes, tracks, audio samples, title,
or creation time according to their documented scope. The observed result is
**20/20 third-party packages and 1/1 browser runtime API passing**. Some
packages parse only a header or metadata field; `mp4-metadata` needs a
`FileReader` compatibility adapter in Node. The ranking labels each scope.

`mp3_id3v2:control` restores a fixed 4997-byte MP3 with one second of 440 Hz
mono audio at 8000 Hz and ID3v2.3 title `Parsarium`, artist `Control`, and
album `Pilot` (SHA-256
`d61e1802a52dc55b5447356a3347fa4f9e08eb706757870f65ee0776dbf5bcad`).
The committed base64 source removes the need for FFmpeg during verification.
Adapters check parsed tags, audio samples, or duration according to each
package's documented scope. The observed result is **24/24 third-party
packages and 2/2 browser runtime APIs passing**. Duration readers disagree
because they account for encoder padding differently; the verification file
records each observed value. The browser APIs decode audio or read duration but
do not expose ID3v2 fields.

`wav:control` creates a deterministic 52-byte mono PCM RIFF/WAVE file with four
16-bit samples at 8000 Hz (SHA-256
`6154e1a5105d7b8b35a7ac228d50907c2fed58ea63577391b34957cc538966ce`).
The WAV adapter checks parsed sample rate, channel count, and either PCM sample
signs, bit depth, or the exact 0.0005-second duration, according to each
documented API's scope. The observed batch result is **22/22 third-party
packages and 1/1 browser-bundled API passing**. Header-only and duration-only
readers are labeled in the ranking. Three header-reader packages report a
duration inconsistent with the control's four samples, so their duration is
not used as verification evidence.

`pdf:control` creates a deterministic 696-byte PDF 1.4 file with one letter-size
page, the title `Parsarium PDF control`, and searchable text `Parsarium`
(SHA-256 `9bbfad1ba7ac5d0f4e25dd1d2e00c9f4cc7a493e303034b5884759f42ec5f60a`).
The PDF adapter checks extracted text or documented page/title fields. The
observed batch result is **22/22 third-party packages passing**. No PDF parser
was found in the scoped Node.js core or browser JavaScript API documentation;
the separate runtime record states those search limits. Browser PDF display
alone does not expose a parsed PDF result to JavaScript.

`http11:control` creates deterministic, valid HTTP/1.1 request and response
wire files. The request is a GET for `/parsarium?x=1` with a Host field; the
response is `200 OK` with the nine-byte body `parsarium` and a matching
Content-Length. The adapter checks parsed method and target or status and body.
The observed batch result is **20/20 third-party packages and 1/1 Node.js
runtime API passing**. Several packages are forks or distributions of the
same underlying parser; the family column records this relationship. The
simple controls establish only these specific parsing paths.

`svg:control` creates a deterministic 196-byte SVG with a red and a green
rectangle in a 2×1 viewport. The adapters check element structure, dimensions,
colors, converted paths, or exact rendered pixels according to each package's
documented scope. The observed batch result is **22/22 third-party packages
passing**. The separate browser run verifies both `DOMParser` with typed SVG
elements and `HTMLImageElement` decoding from a local SVG Blob. A direct
`createImageBitmap(Blob)` attempt failed on the control in this Chromium build;
it is recorded as a candidate failure, not a verified API.

`verify_go_zip.py` uses Go 1.27.1 and the shared deterministic ZIP control.
The Go module at `adapters/go/zip` pins third-party releases in `go.mod` and
checksums in `go.sum`. The adapters check the parsed entry name and
decompressed text. The observed result is **23/23 third-party packages and
1/1 Go standard-library API passing**. Several packages wrap or fork
`archive/zip`; the ranking records their parser families.

`verify_go_png.py` uses Go 1.27.1 and the shared two-pixel PNG control.
`adapters/go/png/go.mod` and `go.sum` pin all Go modules. The bimg and govips
adapters require libvips, and the imagick adapter requires ImageMagick
MagickWand, with their development headers and `pkg-config` files. The
recorded run used libvips 8.18.7 and ImageMagick 7.1.2. Check the local
installation with `pkg-config --modversion vips` and
`pkg-config --modversion MagickWand`. The observed result is **20/20
third-party packages and 3/3 Go standard-library API paths passing**.
Pixel readers, chunk readers, converters, and dimension readers have distinct
scopes in the ranking; several packages share Go's `image/png` decoder or
libvips.

`verify_go_wav.py` uses Go 1.27.1 and the shared four-sample PCM16 WAV control.
`adapters/go/wav/go.mod` and `go.sum` pin the releases. The observed result is
**21/21 third-party packages passing**. The separate Go 1.27.1 standard-library
inventory documents no WAV-aware parser API; generic file and binary readers
do not qualify. The `cryptix/wav` adapter verifies its parsed header and sample
count, since a sample value disagreed with the control's signed PCM.

`verify_go_http11.py` uses Go 1.27.1 and the shared valid request and response
wire controls. `adapters/go/http11/go.mod` and `go.sum` pin the releases. The
observed result is **20/20 third-party packages and 2/2 Go standard-library
API paths passing**. Request-line and request-header-only readers are labeled
by scope. Several packages share `net/http` or `fasthttp` parser lineages;
the package count does not imply 20 independent parser engines.

`verify_go_mp4.py` uses Go 1.27.1 and the shared progressive MP4 control.
`adapters/go/mp4/go.mod` and `go.sum` pin the releases. The observed result is
**20/20 third-party packages passing**. The adapters report parsed movie-box
size, MP4 brand, track or stream count, or title according to the documented
API. The ranking labels narrow `ftyp` and metadata scopes and shared parser
families. The separate standard-library inventory records no MP4-aware API
in the scoped Go 1.27.1 docs.

`verify_go_mp3_id3v2.py` uses Go 1.27.1 and the committed 44.1 kHz MPEG-1
Layer III control with ID3v2.3 title `Parsarium`. Its source bytes are restored
by `python3 controls/mp3_id3v2/make_control.py`, alongside the earlier 8 kHz
control. The observed result is **20/20 third-party packages passing**. Audio
decoders, MPEG frame readers, duration readers, and ID3v2 title readers have
separate scopes in the ranking. Two duration readers include encoder padding in
their reported 1071 ms; one tag reader preserves a trailing NUL in the title.
The Go 1.27.1 standard-library inventory records no MP3 or ID3v2 parser API.

`verify_go_pdf.py` uses Go 1.27.3 and the shared valid one-page PDF control.
`adapters/go/pdf/go.mod` and `go.sum` pin its releases. The observed result is
**20/20 third-party packages passing**. Adapters report page count, extracted
text, PDF version, or parsed indirect-object count according to their documented
scope. Many packages share the rsc PDF reader lineage; the ranking records this.
The separate Go 1.27.3 standard-library inventory documents no PDF document
parser API. The go-fitz adapter uses MuPDF code bundled by its Go module.

`verify_go_svg.py` uses Go 1.27.1 and the shared two-rectangle SVG control.
`adapters/go/svg/go.mod` and `go.sum` pin its releases. The observed result is
**21/21 third-party packages passing**. Adapters report parsed shapes, paths,
viewBox size, rendered pixels, or SVG-aware minified markup according to their
documented scope. Several readers share `oksvg` or Goki/Cogent code lineages.
The separate Go 1.27.1 standard-library inventory finds no SVG-aware parser;
generic XML parsing is outside the cell's parser criterion.

`verify_go_ascii_pnm.py` uses Go 1.27.1 and a valid 2×1 ASCII P3 PPM control
with red and green pixels (SHA-256
`f1e86f7bc611601fed6f44a263d8c1f026dd1d0fd66a7dbc8530e245f5561bf1`).
`make_control.py` also creates valid P1 PBM and P2 PGM files for future
variant-specific checks. The observed result is **20/20 third-party packages
passing on P3**. The ranking labels a header-only reader and dimension-only
native bindings; it does not claim that every package handles all PNM variants.
Five accepted bindings use libvips 8.18.7, and one uses ImageMagick 7.1.2.
Install their development headers and `pkg-config` files before rerunning.
`adapters/go/ascii_pnm/go.mod` and `go.sum` pin dependencies. `go mod verify`
passes; plain `go mod tidy` fails because an upstream `bu/govips` test imports a
removed `davidbyttow/govips` package. Use `go mod tidy -e` if refreshing the
module graph. The separate Go 1.27.1 standard-library inventory records no
PNM-aware parser API.

`verify_go_ascii_ply.py` uses Go 1.27.1 and the valid three-vertex,
one-triangle ASCII PLY control (SHA-256
`d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378`).
The observed result is **21/21 third-party package paths passing**. Nine are
bindings to the Assimp importer and two share the Greg Turk C PLY parser, so
the ranking records 12 parser families. Some readers expose only vertices.
`go.mod` and `go.sum` pin the Go packages; the verifier builds the C PLY
archive from its pinned module and configures the locally installed Assimp
development library through `pkg-config`. The recorded native Assimp version is
6.0.6 on macOS arm64. The separate Go 1.27.1 standard-library inventory finds
no PLY-aware parser API.

`verify_go_matrix_market.py` uses Go 1.27.2 and valid coordinate real general
Matrix Market controls. The observed result is **5/5 eligible package paths
passing**, below the 20-path goal. One reader interprets the matrix as a graph;
another requires local companion row and column index files. The Go module
files pin releases and transitive dependencies, and `go mod verify` passes.
The separate Go 1.27.2 standard-library inventory finds no Matrix Market API.
Seven plausible leads remain unresolved, including one with a successful parse
but no open-source license evidence. See the cell record for exact limits.

`verify_python_png.py` uses CPython 3.13.1 and the two valid local PNG
controls. `requirements.in` pins 21 top-level releases; the generated
`requirements.lock` pins transitive versions and distribution hashes. The
recorded result is **21/21 third-party packages passing**. Pixel decoders,
dimension readers, chunk readers, and a `tEXt` metadata reader have separate
scopes in the ranking. Several packages call Pillow, ImageIO, libvips, or
other native image engines. The run used uv 0.12.19, libvips 8.18.7, and
ImageMagick 7.1.2; the latter two need installed shared libraries. The
verifier sets `MAGICK_HOME` from `pkg-config` for Wand. The Python 3.13
standard/runtime inventory separately verifies Tkinter `PhotoImage` with
bundled Tk 8.6 on the same valid control; it requires a usable GUI session.

`verify_python_ascii_pnm.py` uses the valid 2×1 ASCII P3 red/green PPM and
P2 black/white PGM controls. The pinned, hash-locked Python 3.13 environment
reproduces **20/20 package paths passing**. Eighteen expose P3 pixels, one
exposes P2 grayscale pixels, and one parses P3 header dimensions only. They
include wrappers over Pillow, Qt, and netpbmfile; those shared families are
labeled in the ranking. The verifier also probes bundled Tk 8.6 `PhotoImage`
on valid P1/P2/P3 files and records its three rejections separately from the
package count. `pyvips` and Wand need libvips and ImageMagick shared libraries,
and wxPython/Tk need a GUI session. `napari-netpbmfile` omits a declared
`napari-plugin-engine` dependency; it is pinned explicitly in
`requirements.in`.

`verify_python_ascii_ply.py` verifies **21/21 package paths** on a valid
three-vertex, one-triangle ASCII PLY 1.0 control (SHA-256
`d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378`).
The Python 3.12.14 environment is hash locked. `openmesh` needs CMake and the
stated policy setting when built from source; `pyassimp` loads Homebrew Assimp
6.0.6 on the recorded macOS host. PyVista and vedo use VTK, two packages use
miniply, and two use Assimp; the ranking labels these shared families. The
scoped CPython 3.12 library reference documents no PLY parser API.

`verify_python_zip.py` verifies **20/20 third-party package paths** and
**4/4 CPython standard-library APIs** on valid local ZIP controls. The main
control has a DEFLATE-compressed `hello.txt`; the pinned Zstandard wrapper
generates and reads a method-93 ZIP, and a separate Python-module ZIP tests
`zipimport`. Many packages share CPython's `zipfile` parser family; the
ranking lists those families. `libarchive-c` needs a libarchive shared library,
`patool` needs a local `unzip` utility, and `fs` and `omni-archive` need the
explicit compatibility pins in `requirements.in` for this Python version.

`verify_python_wav.py` verifies **21/21 third-party package paths** and
**1/1 CPython standard-library API** using the four-sample PCM16 WAV control.
The pinned Python 3.13 environment has distribution hashes in
`requirements.lock`. The ranking labels sample readers and WAV metadata
readers, and identifies packages that share CPython `wave`, libsndfile,
FFmpeg, or other backends. Pygame uses a dummy SDL audio driver for its
control run. The standard-library result is `wave.open`.

`verify_python_pdf.py` verifies **20/20 third-party package paths** on the
one-page PDF control. Eighteen packages share the main hash-locked Python 3.13
environment; PDFx and Slate3k use isolated locks because their older
`pdfminer` dependencies conflict with current `pdfminer.six`. The
`pdf2image` and `pdftotext` paths require a local Poppler installation;
the recorded host used Poppler 26.09.0. The ranking distinguishes text,
metadata, layout, and page-rendering results and names shared parser engines.
The scoped CPython standard-library inventory found no PDF-aware input API.

`verify_python_mp3_id3v2.py` verifies **20/20 third-party package paths** on
the tagged one-second MP3 control. The hash-locked Python 3.13 environment
includes ID3 tag readers and MP3 audio decoders; their exact scope and shared
Mutagen, libsndfile, FFmpeg, SDL_mixer, TagLib, and MediaInfo families are
labeled in the ranking. `ffmpeg-python` and `pydub` use local FFmpeg tools;
MoviePy uses its pinned imageio-ffmpeg dependency. The verifier records the
external FFprobe and libsndfile versions. CPython 3.13 documents no MP3 or
ID3v2 input API in its standard library.

`verify_python_mp4.py` verifies **20/20 third-party package paths** on the
one-frame H.264/AAC control. The hash-locked Python 3.13 environment includes
box readers, metadata readers, audio readers, and video frame decoders. The
ranking labels each scope and shared FFmpeg, OpenCV, and other parser families.
Several wrappers need local FFmpeg/FFprobe tools; the verifier records the
external FFprobe version. The scoped CPython 3.13 standard-library inventory
found no MP4-aware input API.

`verify_python_http11.py` verifies **22/22 third-party package paths** and
**3/3 CPython 3.13 standard-library APIs** on valid local HTTP/1.1 request
and response controls. The main hash-locked environment uses Python 3.13;
`http-parser` needs the separate Python 3.10 lock because its C extension
does not build on newer versions here. The ranking identifies shared h11
and picohttpparser families. Two packages parse header fields only, and
`websockets` parses a handshake request head; their scope is explicit in
the catalogue. The standard APIs are `http.client.HTTPConnection.getresponse`,
`http.server.BaseHTTPRequestHandler`, and `http.client.parse_headers`.

`verify_python_svg.py` verifies **20/20 third-party package paths** on two
valid SVG controls: red and green rectangles in a 2×1 viewport, and a red
rectangle with a blue path in a 4×2 viewport. The ranking distinguishes
rendered pixels, element trees, paths, and dimensions, and records shared
resvg/usvg, picosvg, and QtSvg families. CairoSVG, pyvips, and Wand need
installed native Cairo, libvips, and ImageMagick libraries; the verifier sets
their Homebrew library paths on the recorded macOS host. The CPython 3.13.1
standard-library inventory counts no verified SVG API. Official `tkinter`
documentation describes conditional SVG reading with Tk 9.0, while the
recorded runtime has Tk 8.6, so that path remains unresolved.

`verify_python_matrix_market.py` currently verifies **20/20 recorded third-party
package paths**, meeting the working goal. The controls are
valid NIST coordinate matrices: a 2×3 sparse real matrix, a 3×3 graph
adjacency matrix, and a 10x count matrix with feature and barcode files.
The ranking records shared SciPy/fast_matrix_market implementations and leaves
unavailable download metrics unranked. `scprep` runs in a separate Python
3.10 environment because its pinned pandas dependency lacks a compatible
Python 3.13 wheel. `mtl5` also uses Python 3.10 because its Python 3.13
source build lacks a required header. `scab` and `DOTools-py` pass in the
Python 3.13 environment after building `annoy` with `CXXFLAGS='-include functional'`.
`piaso-tools` 1.2.6 builds its Rust extension from source on this macOS arm64
host, so reproducing that environment requires Cargo.
Three documented or plausible leads remain unresolved; discovery remains partial.
The scoped CPython 3.13 standard-library inventory found no
Matrix Market-aware input API.

`verify_rust_png.py` uses Rust 1.99.1 and Cargo's locked dependency graph at
`adapters/rust/png/Cargo.lock`. It builds the Rust adapter with
`cargo build --locked` and runs 21 pinned crate paths against the valid two-pixel PNG or
its `Title=Parsarium` tEXt variant. All **21/21** passed, returning decoded
pixels, dimensions, chunks, or metadata according to each documented API.
They represent 17 recorded parser families or lineages; wrappers and a fork
are identified in the ranking. The scoped Rust standard library has no
documented PNG parser. Ten plausible leads remain unresolved, including
some with higher adoption counts, and the registry search is partial.

`verify_rust_zip.py` uses Rust 1.99.1 and the pinned Cargo graph at
`adapters/rust/zip/Cargo.lock`. It builds with `cargo build --locked` and
runs **20/20** crate paths against the valid one-entry DEFLATE ZIP control.
Most adapters check the parsed entry name, declared size, and decompressed
text; `archiver-rs` checks entry names and `zip_structs` checks a local header.
The 20 package paths represent 12 recorded parser families or lineages.
`libarchive2-sys` builds vendored libarchive with CMake and bindgen, requiring
a C compiler, CMake, and libclang. The scoped Rust standard library has no
documented ZIP parser. Ten plausible leads remain unresolved.

`verify_rust_mp4.py` builds the pinned Rust MP4 graph with `cargo build --locked`
and runs **21/21** crate paths against a valid MP4 with H.264 video, AAC audio,
and a title tag. Each row names its track, box, audio, or metadata scope and
records shared mp4-rs, mp4parse, and Symphonia lineages. The scoped Rust
standard library has no documented MP4 parser. Ten plausible leads remain
unresolved; the seven bounded registry searches are partial.

`verify_rust_wav.py` builds the pinned Rust WAV graph with `cargo build --locked`
and runs **20/20** crate paths against a valid 8 kHz mono, four-sample PCM WAV.
The paths include sample decoders, WAV header and chunk readers, and demuxers;
their precise scopes and shared Hound and Symphonia families are recorded in
`data/rust/wav/parsers.json`. The scoped Rust standard library has no
documented WAV parser. Thirteen plausible leads remain unresolved.

`verify_rust_pdf.py` builds the pinned Rust PDF graph with `cargo build --locked`
and runs **21/21** crate paths against a valid one-page PDF 1.4 with searchable
text and an Info title. The paths include page-tree readers, document facades,
and a text extractor; their shared lopdf, pdfrum, and zpdf families are
recorded in `data/rust/pdf/parsers.json`. The scoped Rust standard library
has no documented PDF parser. Ten plausible leads remain unresolved.

`verify_rust_svg.py` builds the pinned Rust SVG graph with `cargo build --locked`
and runs **25/25** crate paths against valid SVG rectangle and path controls.
The `librsvg` crate requires Cairo, PangoCairo, and GLib development libraries;
the recorded macOS run resolved them through `pkg-config`.
Twenty accept a complete SVG document; five accept only extracted SVG path data.
The paths cover document trees, rendered pixels and scene commands, metadata,
and explicitly scoped path data. Several packages share usvg, svgtypes,
or svgdom lineages, as recorded in `data/rust/svg/parsers.json`. The scoped Rust
standard library has no documented SVG parser. Two plausible leads remain
unresolved, and the seven bounded registry searches are partial.

`verify_rust_http11.py` builds the pinned Rust HTTP/1.1 graph with
`cargo build --locked` and runs **22/22** crate paths against valid local
request and response wire controls. Eighteen paths parse requests and four
parse responses. The result is a package-path count: several crates depend on
httparse, ntex-httparse is its fork, and two paths share node/http-parser lineage.
The ranking records these shared families
and the narrower request-line scope of ntex-httparse. The scoped Rust standard
library has no documented HTTP/1.1 message parser. Four plausible leads remain
unresolved, and the bounded registry search is partial.

`verify_rust_ascii_ply.py` builds the pinned Rust ASCII PLY graph with
`cargo build --locked` and runs **20/20** crate paths against valid triangle,
unsigned face-index, and coloured point-cloud controls. The paths report
vertices, faces, coordinates, colours, or format according to their input API.
Several wrappers use ply-rs or its ply-rs-bw fork; threecrate re-exports
threecrate-io. The ranking records these families and vertex-only scopes.
The scoped Rust standard library has no documented ASCII PLY parser. Four
plausible leads remain unresolved, and the bounded registry search is partial.

`verify_rust_ascii_pnm.py` builds pinned Rust ASCII PNM adapters and runs
**21/21** crate paths against valid P1, P2, and P3 controls. It records RGB,
grayscale, QR payload, or header-dimension results according to each API's
scope. The `include-pnm` path compiles the supplied control at build time;
`pnm` 0.1.1 requires `RUSTC_BOOTSTRAP=1`; and `fltk` builds its native FLTK
loader through the pinned `fltk-sys` crate. To regenerate the P1 QR control,
run `cargo build --locked --manifest-path adapters/rust/ascii_pnm/Cargo.toml`
and `adapters/rust/ascii_pnm/target/debug/make_qr_control controls/ascii_pnm/qr-p1.pbm`.
The scoped Rust standard library has no documented ASCII PNM parser. Three
plausible leads remain unresolved, and the bounded registry search is partial.

`verify_rust_matrix_market.py` builds two locked Rust adapters and runs
**20/20** crate paths against valid coordinate real general, coordinate real
symmetric, and gzip-compressed 10x integer controls. It records shapes, entries,
and selected values according to each API's scope. `powerio-matrix` uses `sprs`;
`hybit` re-exports `hybit-matrix`. The separate Rust standard-library inventory
finds no documented Matrix Market parser. Four plausible leads remain unresolved,
including the higher-download `bixverse-sc-data` path.

`verify_rust_mp3_id3v2.py` builds the pinned Rust MP3 graph with
`cargo build --locked` and runs **20/20** crate paths against a valid tagged
MPEG Layer III control. Each row labels its tag, frame, duration, or decoded
audio scope, and shared Symphonia, minimp3, and id3 paths. The scoped Rust
standard library has no documented MP3 or ID3v2 parser. Twelve plausible
leads remain unresolved.

To refresh *discovery and popularity* data, run
`node scripts/snapshot_npm.mjs png`, `zip`, `mp4`, `mp3_id3v2`, `wav`, `pdf`, `svg`, `http11`, `ascii_pnm`, or `ascii_ply`.
Run `node scripts/triage_npm.mjs png`, `zip`, `mp4`, `mp3_id3v2`, `wav`, `pdf`, `svg`, `http11`, `ascii_pnm`, or `ascii_ply`
to refresh popularity-sorted **leads**; triage never verifies a parser.
This is a separate, network-dependent operation that changes the dated registry
snapshot; verification itself uses only locked local dependencies. npm's
[search API](https://github.com/npm/registry/blob/main/docs/REGISTRY-API.md)
supplies discovery hits. Its [downloads API](https://github.com/npm/registry/blob/main/docs/download-counts.md)
supplies the single ranking metric. The metric is the number of registry
downloads during **2026-10-11 through 2026-11-09**, inclusive, for each package
name. It is an adoption proxy and can include automated downloads.

For Go ZIP, PNG, WAV, HTTP/1.1, MP4, MP3 with ID3v2, PDF, SVG, or ASCII PNM discovery, install the pinned packages in
`scripts/requirements-go-discovery.txt`, then run `python3 scripts/snapshot_go.py FORMAT`
and `python3 scripts/enrich_go.py FORMAT` with `FORMAT` set to `zip`, `png`,
`wav`, `http11`, `mp4`, `mp3_id3v2`, `pdf`, `svg`, or `ascii_pnm`. These refresh bounded pkg.go.dev
package-search hits, pinned-release license evidence, and package-level
“Imported by” counts. Go counts are compared only within their Go format cell.
The public search pages supplied this snapshot after the
[pkg.go.dev API](https://pkg.go.dev/v1/api) returned a rate limit response.

For Python PNG, ASCII PLY, ASCII PNM, ZIP, WAV, PDF, MP3 with ID3v2, MP4, HTTP/1.1, SVG, or Matrix Market discovery, run
`python3 scripts/snapshot_pypi_png.py`,
`python3 scripts/snapshot_pypi_ascii_ply.py`, or
`python3 scripts/snapshot_pypi_ascii_pnm.py`, or
`python3 scripts/snapshot_pypi_zip.py`, or
`python3 scripts/snapshot_pypi_wav.py`, or
`python3 scripts/snapshot_pypi_pdf.py`, or
`python3 scripts/snapshot_pypi_mp3_id3v2.py`, or
`python3 scripts/snapshot_pypi_mp4.py`, or
`python3 scripts/snapshot_pypi_http11.py`, or
`python3 scripts/snapshot_pypi_svg.py`, or
`python3 scripts/snapshot_pypi_matrix_market.py`. Each
filters the [PyPI Simple JSON project index](https://docs.pypi.org/api/index-api/)
by recorded name terms, saves the first 100 alphabetic matches per term, and
fetches pinned release metadata. [PyPI Stats](https://pypistats.org/api/)
provides its `last_month` download signal, excluding known mirrors. The
index is not relevance ranked, and the download signal is compared only
within Python. Unavailable metrics remain `null`.

For Rust PNG, ZIP, MP4, WAV, PDF, SVG, HTTP/1.1, ASCII PLY, ASCII PNM, Matrix Market, or MP3 with ID3v2 discovery, run `python3 scripts/snapshot_crates.py FORMAT` and
`python3 scripts/enrich_rust.py FORMAT`, with `FORMAT` set to `png`, `zip`, `mp4`, `wav`, `pdf`, `svg`, `http11`, `ascii_ply`, `ascii_pnm`, `matrix_market`, or `mp3_id3v2`, to refresh seven bounded
[crates.io API](https://crates.io/api/) searches, pinned release metadata,
and crate-level recent downloads over about 90 days. The downloads are
compared only within each Rust format cell. These commands require network access and
replace the dated snapshot; the locked control verification does not.

## Verified rankings and search limits

The working goal is 20 verified third-party parsers per cell, with 30 as the
original ceiling. The JavaScript PNG and ZIP cells have **21 verified packages** each;
the WAV, PDF, and SVG cells have **22** each, MP4 and HTTP/1.1 have **20** each,
MP3 with ID3v2 has **24**, and ASCII PNM has **22**.
Packages verified after the twentieth row are kept in
the collection. Package downloads are an adoption proxy, not a security
or quality judgment.

- [JavaScript × PNG ranking](data/javascript/png/ranking.md): 21 packages,
  including header-only and chunk-only parsers labeled by scope. Four npm queries
  saved the first 100 results each: 400 hits, 344 unique names. Ten named leads
  remain unresolved. The [runtime inventory](data/javascript/png/standard.json)
  separately verifies browser `createImageBitmap(Blob)` and records the scoped
  Node.js 26.10.0 built-in API finding. The browser API is specified by the
  [HTML Standard](https://html.spec.whatwg.org/multipage/imagebitmap-and-animations.html#dom-createimagebitmap-dev).
- [JavaScript × ZIP ranking](data/javascript/zip/ranking.md): 21 packages, each
  returning the entry name and decompressed text. Four npm queries saved the
  first 100 results each: 400 hits, 314 unique names. Four named leads remain
  unresolved. The [Node.js `zlib.ZipBuffer` API](https://nodejs.org/docs/v26.10.0/api/zlib.html#class-zlibzipbuffer)
  is experimental and verified separately from the npm ranking.
- [JavaScript × MP4 ranking](data/javascript/mp4/ranking.md): 20 packages with
  labeled box, metadata, track, or audio decode scope. Five npm queries saved
  the first 100 hits each: 500 hits, 372 unique names. Fifteen named leads
  remain unresolved. The browser `HTMLVideoElement` metadata API is verified
  separately with a local MP4 Blob; see the
  [runtime inventory](data/javascript/mp4/standard.json).
- [JavaScript × MP3 with ID3v2 ranking](data/javascript/mp3_id3v2/ranking.md):
  24 packages with tag, audio decode, or duration scope. Five npm queries saved
  495 hits, 447 unique names; the first query returned only 95 hits and the
  other four stopped at 100. Ten named leads remain unresolved. The
  [runtime inventory](data/javascript/mp3_id3v2/standard.json) separately
  verifies browser audio decoding and media metadata on the tagged control.
- [JavaScript × WAV ranking](data/javascript/wav/ranking.md): 22 packages with
  explicitly labeled sample, header, or duration scope. Four npm queries saved
  the first 100 results each: 400 hits, 351 unique names. Five relevant leads
  remain unresolved. The separate [runtime inventory](data/javascript/wav/standard.json)
  verifies Chromium's `OfflineAudioContext.decodeAudioData(ArrayBuffer)` on the
  same control, using the [Web Audio specification](https://www.w3.org/TR/webaudio-1.1/#dom-baseaudiocontext-decodeaudiodata).
- [JavaScript × PDF ranking](data/javascript/pdf/ranking.md): 22 packages,
  including text extraction, page metadata, and page count APIs. Four npm queries
  saved the first 100 results each: 400 hits, 347 unique names. Twelve relevant
  leads remain unresolved. Shared PDF.js wrappers are grouped by family. The
  [runtime inventory](data/javascript/pdf/standard.json) documents the scoped
  absence of a public PDF parsing API in Node.js core and browser standards.
- [JavaScript × HTTP/1.1 ranking](data/javascript/http11/ranking.md): 20 packages
  parsing a request or response control. Six npm queries saved the first 100
  results each: 600 hits, 268 unique names. Eight named leads remain unresolved.
  The [runtime inventory](data/javascript/http11/standard.json) separately
  verifies Node.js `node:http.createServer` using the local request bytes.
- [JavaScript × SVG ranking](data/javascript/svg/ranking.md): 22 packages
  spanning structure, dimensions, colors, paths, and rendered pixels. Four npm
  queries saved 400 hits, 388 unique names. Twelve named leads remain
  unresolved. The [runtime inventory](data/javascript/svg/standard.json)
  separately verifies browser SVG DOM parsing and image decoding.
- [JavaScript × ASCII PNM ranking](data/javascript/ascii_pnm/ranking.md):
  22 verified package paths on valid P3 or P2 controls, with pixel, dimension,
  and format metadata scopes labeled. Eight bounded npm queries saved 658 hits and
  458 distinct names; two explored leads remain unresolved. The
  [runtime inventory](data/javascript/ascii_pnm/standard.json) records scoped
  Node.js and Chromium findings. Shared `image-size` parser families are labeled.
- [JavaScript × ASCII PLY ranking](data/javascript/ascii_ply/ranking.md):
  20 verified package paths on the valid three-vertex triangle control. Seventeen
  return triangle faces; three return vertex or point-cloud records. Seven
  Three.js-derived paths, two loaders.gl paths, and two voxelkloud paths are
  marked as shared parser families, leaving 12 families in total. Ten bounded
  npm queries saved 870 hits and 706 distinct names; six explored leads remain
  unresolved. The [runtime inventory](data/javascript/ascii_ply/standard.json)
  records the scoped absence of a PLY-aware Node.js or browser platform API.
- [JavaScript × Matrix Market ranking](data/javascript/matrix_market/ranking.md):
  seven pinned packages verified on valid local coordinate real general,
  symmetric, or 10x Matrix Market controls, 13 below the working goal. Six
  bounded npm queries saved 406 hits and 353 distinct names; three plausible
  leads remain unresolved. `scran.js` and `bakana` share the same underlying
  WASM reader; `@orbifold/graphs` was verified only on a no-comment control. The
  [cell record](data/javascript/matrix_market/cell.json) gives the exact scope.
- [Go × ZIP ranking](data/go/zip/ranking.md): 23 packages spanning direct ZIP
  readers, streaming readers, and extraction wrappers. Five pkg.go.dev queries
  saved 333 hits, 271 unique package paths. Eight named leads remain
  unresolved. The [standard-library inventory](data/go/zip/standard.json)
  separately verifies `archive/zip.OpenReader` on the same control.
- [Go × PNG ranking](data/go/png/ranking.md): 20 packages spanning pixel,
  chunk, and dimension readers. Five pkg.go.dev queries saved 321 hits and
  228 unique package paths. Five named leads remain unresolved. The
  [standard-library inventory](data/go/png/standard.json) separately verifies
  `image/png.Decode`, `DecodeConfig`, and registered `image.Decode`.
- [Go × WAV ranking](data/go/wav/ranking.md): 21 packages with labeled sample,
  header, and data-size scopes. Five pkg.go.dev queries saved 373 hits and
  271 unique package paths; eight named leads remain unresolved. The
  [standard-library inventory](data/go/wav/standard.json) records the scoped
  Go 1.27.1 finding.
- [Go × HTTP/1.1 ranking](data/go/http11/ranking.md): 20 packages with labeled
  request-message, header, and request-line scopes. Six pkg.go.dev queries saved
  404 hits and 364 unique package paths; ten named leads remain unresolved.
  The [standard-library inventory](data/go/http11/standard.json) separately
  verifies `net/http.ReadRequest` and `ReadResponse`.
- [Go × MP4 ranking](data/go/mp4/ranking.md): 20 packages with labeled box,
  track, stream, and title scopes. Five pkg.go.dev queries saved 133 hits and
  124 unique package paths; ten plausible leads remain unresolved, including
  fragmented-MP4 readers requiring a separate valid control. The
  [standard-library inventory](data/go/mp4/standard.json) records the scoped
  Go 1.27.1 finding.
- [Go × MP3 with ID3v2 ranking](data/go/mp3_id3v2/ranking.md): 20 packages with
  labeled audio, MPEG frame, duration, and ID3 title scopes. Five pkg.go.dev
  queries saved 311 hits and 252 unique package paths; ten plausible leads
  remain unresolved. The [standard-library inventory](data/go/mp3_id3v2/standard.json)
  records the scoped Go 1.27.1 finding.
- [Go × PDF ranking](data/go/pdf/ranking.md): 20 packages with labeled page,
  text, version, or object scope. Five pkg.go.dev queries saved 462 hits and
  384 unique package paths; ten plausible leads remain unresolved, including
  a native PDFium binding and a reader that failed to compile with the pinned
  pdfcpu version. The [standard-library inventory](data/go/pdf/standard.json)
  records the scoped Go 1.27.3 finding.
- [Go × SVG ranking](data/go/svg/ranking.md): 21 packages with labeled shape,
  path, viewBox, raster, or SVG minification scope. Five pkg.go.dev queries saved
  322 hits and 280 unique package paths; ten plausible leads remain unresolved.
  One higher-adoption reader could not link because the host lacked MoltenVK.
  The [standard-library inventory](data/go/svg/standard.json) records the scoped
  Go 1.27.1 finding.
- [Go × ASCII PNM ranking](data/go/ascii_pnm/ranking.md): 20 packages verified
  on the valid P3 control, with pixels, dimensions, or header fields as labeled.
  Five pkg.go.dev queries saved 156 hits and 141 unique package paths; ten
  plausible leads remain unresolved. Five accepted bindings share libvips,
  and several modules share Go PNM code. The
  [standard-library inventory](data/go/ascii_pnm/standard.json) records the
  scoped Go 1.27.1 finding.
- [Go × ASCII PLY ranking](data/go/ascii_ply/ranking.md): 21 package paths
  verified on the valid triangle control, representing 12 recorded parser
  families. Six pkg.go.dev queries saved 83 hits and 81 unique paths; two
  plausible leads remain unresolved. The
  [standard-library inventory](data/go/ascii_ply/standard.json) records the
  scoped Go 1.27.1 finding.
- [Go × Matrix Market ranking](data/go/matrix_market/ranking.md): seven eligible
  package paths verified on local coordinate real general or pattern symmetric
  controls, 13 below
  the working goal. Six bounded pkg.go.dev queries saved 80 hits and 77 unique
  paths; five plausible leads remain unresolved. Two pinned packages use Go
  module replacements because their published module names differ from their
  repository paths; their adoption metric is unavailable. The
  [cell record](data/go/matrix_market/cell.json) states search and input limits.
- [Python × PNG ranking](data/python/png/ranking.md): 21 packages verified
  on local pixel or text-chunk controls. Seven bounded PyPI name filters
  saved 379 distinct project names; eight plausible leads remain unresolved.
  One verified package lacks a PyPI Stats figure and is left unranked. The
  [standard/runtime inventory](data/python/png/standard.json) separately
  verifies Tkinter `PhotoImage` and records its platform limit.
- [Python × ASCII PLY ranking](data/python/ascii_ply/ranking.md): 21 package
  paths parsed the triangle control. Twelve bounded PyPI name windows saved
  668 hits and 666 distinct names; seven plausible leads remain unresolved.
  VTK, miniply, and Assimp wrappers are grouped by parser family. The
  [standard-library inventory](data/python/ascii_ply/standard.json) records
  the scoped CPython finding.
- [Python × ASCII PNM ranking](data/python/ascii_pnm/ranking.md): 20 package
  paths verified on valid P3 or P2 controls, with pixel or header scopes
  labeled. Twelve bounded PyPI name filters saved 675 hits and 669 distinct
  project names; six plausible leads remain unresolved. One verified package
  initially hit a PyPI Stats rate limit; a successful retry supplied its figure. The
  [standard/runtime inventory](data/python/ascii_pnm/standard.json) records
  Tkinter's failed ASCII controls and the scoped CPython finding.
- [Python × ZIP ranking](data/python/zip/ranking.md): 20 package paths verified
  on valid DEFLATE or Zstandard ZIP controls. Nine bounded PyPI name filters
  saved 418 hits and 407 distinct names; six plausible leads remain unresolved.
  The higher-download `zipfile-deflate64` lead failed to build on this host and
  was not counted. The [standard/runtime inventory](data/python/zip/standard.json)
  separately verifies four documented CPython API paths.
- [Python × WAV ranking](data/python/wav/ranking.md): 21 package paths verified
  on the PCM16 control, with sample and metadata scopes labeled. Nine bounded
  PyPI name filters saved 782 hits and 688 distinct names; five plausible
  leads remain unresolved, including torchaudio. The
  [standard-library inventory](data/python/wav/standard.json) separately
  verifies `wave.open`.
- [Python × PDF ranking](data/python/pdf/ranking.md): 20 package paths verified
  on the valid one-page control. Nine bounded PyPI name filters saved 677
  hits and 672 distinct names; nine plausible leads remain unresolved. Shared
  PDF engines are labeled, and the
  [standard-library inventory](data/python/pdf/standard.json) records the
  scoped absence of a CPython PDF parser API.
- [Python × MP3 with ID3v2 ranking](data/python/mp3_id3v2/ranking.md):
  20 package paths verified on the tagged MP3 control. Nine bounded PyPI
  name filters saved 840 hits and 741 distinct names; six plausible leads
  remain unresolved. Tag readers and audio decoders have separate scope labels,
  and the [standard-library inventory](data/python/mp3_id3v2/standard.json)
  records the scoped CPython finding.
- [Python × MP4 ranking](data/python/mp4/ranking.md): 20 package paths
  verified on the one-frame audiovisual control. Nine bounded PyPI name
  filters saved 672 hits and 667 distinct names; eight plausible leads remain
  unresolved. Box, metadata, audio, and frame scopes are labeled, and the
  [standard-library inventory](data/python/mp4/standard.json) records the
  scoped CPython finding.
- [Python × SVG ranking](data/python/svg/ranking.md): 20 package paths
  verified on the two valid SVG controls. Sixteen bounded PyPI name filters
  saved 710 hits and 676 distinct names; four explored leads remain unresolved.
  Shared parser families and the conditional Tk 9.0 runtime finding are
  recorded in the [cell record](data/python/svg/cell.json).
- [Python × Matrix Market ranking](data/python/matrix_market/ranking.md):
  twenty verified package paths. Thirteen bounded PyPI name filters
  saved 379 hits and 378 distinct names; three explored leads remain
  unresolved. Targeted documentation searches found three additional readers.
  The [cell record](data/python/matrix_market/cell.json) names the untested
  format variants.
- [Rust × PNG ranking](data/rust/png/ranking.md): 21 verified crate paths,
  representing 17 families or lineages. Seven bounded crates.io searches
  saved 650 hits and 459 distinct names; ten explored leads remain
  unresolved. The [cell record](data/rust/png/cell.json) records the search
  limits and the separate standard-library inventory.
- [Rust × ZIP ranking](data/rust/zip/ranking.md): 20 verified crate paths,
  representing 12 families or lineages. Seven bounded crates.io searches
  saved 526 hits and 384 distinct names; ten plausible leads remain
  unresolved. The [cell record](data/rust/zip/cell.json) records the search
  limits and the separate standard-library inventory.
- [Rust × MP4 ranking](data/rust/mp4/ranking.md): 21 verified crate paths.
  Seven bounded crates.io searches saved 552 hits and 340 distinct names;
  ten plausible leads remain unresolved. The [cell record](data/rust/mp4/cell.json)
  records the search limits and separate standard-library inventory.
- [Rust × WAV ranking](data/rust/wav/ranking.md): 20 verified crate paths.
  Seven bounded crates.io searches saved 653 hits and 469 distinct names;
  13 plausible leads remain unresolved. The [cell record](data/rust/wav/cell.json)
  records the search limits and separate standard-library inventory.
- [Rust × PDF ranking](data/rust/pdf/ranking.md): 21 verified crate paths.
  Seven bounded crates.io searches saved 700 hits and 443 distinct names;
  ten plausible leads remain unresolved. The [cell record](data/rust/pdf/cell.json)
  records the search limits and separate standard-library inventory.
- [Rust × SVG ranking](data/rust/svg/ranking.md): 25 verified crate paths, 20 of
  which accept complete SVG documents and five only SVG path data.
  Seven bounded crates.io searches saved 700 hits and 524 distinct names;
  two plausible leads remain unresolved. The [cell record](data/rust/svg/cell.json)
  records path-data scope, search limits, and the separate standard-library inventory.
- [Rust × HTTP/1.1 ranking](data/rust/http11/ranking.md): 22 verified crate paths:
  18 request and four response parsers. Seven bounded crates.io searches saved
  638 hits and 514 distinct names; four plausible leads remain unresolved. The
  [cell record](data/rust/http11/cell.json) records shared families, search
  limits, and the separate standard-library inventory.
- [Rust × ASCII PLY ranking](data/rust/ascii_ply/ranking.md): 20 verified crate
  paths. Seven bounded crates.io searches saved 484 hits and 297 distinct
  names; four plausible leads remain unresolved. The
  [cell record](data/rust/ascii_ply/cell.json) records family relationships,
  scope, search limits, and the separate standard-library inventory.
- [Rust × ASCII PNM ranking](data/rust/ascii_pnm/ranking.md): 21 verified crate
  paths. Seven bounded crates.io searches saved 425 hits and 306 distinct
  names; three plausible leads remain unresolved. The
  [cell record](data/rust/ascii_pnm/cell.json) identifies header-only scope,
  shared families, search limits, and the separate standard-library inventory.
- [Rust × Matrix Market ranking](data/rust/matrix_market/ranking.md): 20 verified
  crate paths. Seven bounded crates.io searches saved 474 hits and 403 distinct
  names; four plausible leads remain unresolved. The
  [cell record](data/rust/matrix_market/cell.json) records input variants,
  shared families, search limits, and the separate standard-library inventory.
- [Rust × MP3 with ID3v2 ranking](data/rust/mp3_id3v2/ranking.md): 20 verified
  crate paths. Seven bounded crates.io searches saved 676 hits and 430
  distinct names; 12 plausible leads remain unresolved. The
  [cell record](data/rust/mp3_id3v2/cell.json) records search limits and the
  separate standard-library inventory.

The full discovery surfaces have not been exhausted. The [PNG cell record](data/javascript/png/cell.json)
and [ZIP cell record](data/javascript/zip/cell.json), along with the
[WAV cell record](data/javascript/wav/cell.json) and
[PDF cell record](data/javascript/pdf/cell.json), and
[HTTP/1.1 cell record](data/javascript/http11/cell.json), and
[SVG cell record](data/javascript/svg/cell.json), and
[MP4 cell record](data/javascript/mp4/cell.json), and
[MP3 with ID3v2 cell record](data/javascript/mp3_id3v2/cell.json) state the actual counts,
search limits, and remaining uncertainty. Registry hits and download counts are
not parser evidence; only the pinned APIs and successful control runs enter the
rankings.
The [Go ZIP cell record](data/go/zip/cell.json) gives its separate count,
search limits, and uncertainty.
The [Go PNG cell record](data/go/png/cell.json) gives the corresponding
PNG-specific limits and uncertainty.
The [Go WAV cell record](data/go/wav/cell.json) gives the WAV search limits and
uncertainty.

## Data layout

- `data/cells.json`: every ecosystem × format cell, with status, actual verified
  count, search limit, and uncertainty.
- `data/go/zip/`: bounded pkg.go.dev search hits, pinned module and license
  evidence, package importer counts, verified ranking, leads, standard API,
  and control results. `adapters/go/zip/go.mod` and `go.sum` pin dependencies.
- `data/go/png/`: the same evidence layout for Go PNG; native libvips and
  MagickWand dependencies are stated above.
- `data/go/wav/`: bounded registry search, pinned releases, per-package WAV
  control outputs, ranking, leads, and the separate standard-library finding.
- `data/go/ascii_pnm/`: bounded search hits, pinned releases, package-level
  importer counts, P3 control outputs, ranking, leads, and standard-library
  finding. Native adapters live under `adapters/go/ascii_pnm/`.
- `data/python/png/`: PyPI name-index leads, pinned release hashes,
  within-Python download signals, verified ranking, standard-library
  inventory, and control outputs. Python dependencies and the adapter live
  under `adapters/python/png/`.
- `data/python/ascii_ply/`: bounded PyPI leads, pinned releases, download
  metrics, control results, ranking, and the scoped CPython inventory. The
  adapter and hash-locked dependencies live under `adapters/python/ascii_ply/`.
- `data/python/ascii_pnm/`: the same evidence layout for ASCII PNM, with
  P3/P2 control output and the Tk runtime candidate result. Python adapters
  and pinned dependencies live under `adapters/python/ascii_pnm/`.
- `data/python/zip/`: bounded PyPI leads, pinned release hashes, within-Python
  download counts, a verified ranking, control outputs, and four standard APIs.
  The adapters and dependency lock live under `adapters/python/zip/`.
- `data/python/wav/`: bounded PyPI leads, pinned release hashes, within-Python
  downloads, sample and metadata scopes, control outputs, and the separate
  standard-library result. The adapters and lock live under
  `adapters/python/wav/`.
- `data/python/pdf/`: bounded PyPI leads, three pinned Python environments,
  within-Python downloads, verified text/metadata/layout/rendering scopes,
  control outputs, and the separate standard-library finding.
- `data/python/mp3_id3v2/`: bounded PyPI leads, a hash-locked Python
  environment, within-Python downloads, tag and audio scopes, control outputs,
  and the separate standard-library finding.
- `data/python/mp4/`: bounded PyPI leads, a hash-locked Python environment,
  within-Python downloads, MP4 box/metadata/audio/video scopes, control
  outputs, and the separate standard-library finding.
- `data/java/zip/`: bounded Maven Central search attempts, targeted pinned
  release lookups, version-level direct-dependent counts, verified ZIP control
  outputs, ranking, and separate JDK 21 API results. The Java adapter and
  resolved-JAR hash lock live under `adapters/java/zip/`.
- `data/java/png/`: the equivalent pinned Maven release, ranking, control,
  and JDK 21 PNG API evidence. The macOS arm64 adapter and JAR lock live under
  `adapters/java/png/`.
- `data/java/mp3_id3v2/`: twenty pinned Maven release paths, three valid tagged
  MP3 controls, exact-release direct-dependent ranking, one unresolved lead,
  and a separate JDK-only probe. Nine adapters and their resolved-JAR hash
  locks live under `adapters/java/mp3_id3v2/`. All five bounded Maven search
  queries timed out, so the most-used top 20 remains uncertain.
- `data/php/zip/`: Packagist discovery hits, pinned Composer releases, lifetime
  download ranking, control results, leads, and separate PHP runtime APIs. The
  adapters and six Composer locks live under `adapters/php/zip/`.
- `data/php/png/`: Packagist discovery hits, pinned Composer releases, lifetime
  download ranking, control results, leads, and four separate PHP runtime APIs.
  The adapters and Composer lock live under `adapters/php/png/`.
- `data/php/ascii_pnm/`: Packagist discovery hits, twenty pinned third-party
  paths, lifetime download ranking, control results, leads, and a separate PHP
  runtime inventory. Eight Composer locks live under `adapters/php/ascii_pnm/`,
  and a pinned PECL Imagick source lock lives with the cell data.
- `data/php/mp3_id3v2/`: Packagist discovery hits, twenty pinned third-party
  paths, lifetime download ranking, valid tag results, unresolved leads, and a
  separate PHP runtime inventory. Seventeen Composer locks and the adapter live under
  `adapters/php/mp3_id3v2/`.
- `data/php/wav/`: Packagist WAV discovery hits, twenty pinned parser paths,
  control results, unresolved leads, lifetime download ranking, and a separate
  PHP runtime inventory. Its adapter reuses the exact Composer locks listed in
  `adapters/php/mp3_id3v2/`.
- `data/php/pdf/`: Packagist PDF discovery hits, twenty pinned parser paths,
  control results, unresolved leads, lifetime download ranking, and a separate
  PHP runtime inventory. Its Composer lock and adapter live in `adapters/php/pdf/`.
- `data/php/svg/`: bounded Packagist SVG discovery hits, twenty pinned parser
  paths, lifetime download ranking, replay results, unresolved leads, and two
  separate PHP 8.5 runtime APIs. Twenty Composer locks and the adapters live under
  `adapters/php/svg/`.
- `data/javascript/{png,zip,mp4,mp3_id3v2,wav,pdf,svg,http11}/registry-snapshot.json`: dated registry hits, pinned
  release metadata, and comparable download counts. A hit is not verification.
- `data/javascript/{png,zip,mp4,mp3_id3v2,wav,pdf,svg,http11}/triage.json`: popularity-sorted discovery leads,
  including unresolved names; the status distinguishes verified packages.
- `data/javascript/{png,zip,mp4,mp3_id3v2,wav,pdf,svg,http11}/parsers.json`: pinned packages, documented input APIs,
  parsing depth, licenses, and shared families.
- `data/javascript/{png,zip,mp4,mp3_id3v2,wav,pdf,svg,http11}/ranking.md`: generated rankings using only verified
  package rows and the recorded metric window.
- `adapters/javascript/` and `controls/`: runnable local-input adapters and
  deterministic valid controls.
- `data/javascript/{png,zip,mp4,mp3_id3v2,wav,pdf,svg,http11}/verification.json` and `png/browser-verification.json`:
  observed outputs, environment, and pass/fail result.

This collection does not contain malformed-input, security, or resource-use
experiments.
