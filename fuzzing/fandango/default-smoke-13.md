# Default Fandango route smoke

On 17 November 2026, Fandango 1.3.1 generated one fixed-seed (`7`) file for
each of the ten active formats and three pilots. Each file completed a
one-input replay, each project prepared an AFL++ plan, and every plan passed
`afl run --check`. [The machine receipt](default-smoke-13.json) records the
exact project, spec SHA-256, output SHA-256, image IDs, replay result, and
plan check. No AFL++ campaign was started.

| Format | Verified target | Default spec | Replay / AFL check |
| --- | --- | --- | --- |
| PNG | `cpp/opencv` | Fanbase `png` | 1/1 / ready |
| ZIP | `cpp/poco` | Fanbase `zip` | 1/1 / ready |
| MP4 | `cpp/exiv2` | local `mp4.fan` | 1/1 / ready |
| WAV | `c/dr_wav` | Fanbase `wav` | 1/1 / ready |
| PDF | `cpp/poppler` | local `pdf.fan` | 1/1 / ready |
| SVG | `c/librsvg` | local `svg.fan` | 1/1 / ready |
| HTTP/1.1 | `cpp/poco` | local `http11_request.fan` | 1/1 / ready |
| ASCII PLY | `c/assetkit` | local `ascii_ply.fan` | 1/1 / ready |
| ASCII PNM | `cpp/openimageio` | local `ascii_pnm_p3.fan` | 1/1 / ready |
| MP3, ID3v2-tagged control | `c/mpv` | local `mp3_tagged.fan` | 1/1 / ready |
| JSON pilot | `python/simplejson` | Fanbase `json` | 1/1 / ready |
| XML pilot | `python/xmltodict` | Fanbase `xml` | 1/1 / ready |
| MP3, untagged controls | `go/github_com_dmulholl_mp3lib` | local `mp3_plain.fan` | 1/1 / ready |

To repeat the smoke from the repository root, install the pinned Fandango
environment and build the selected Docker and AFL++ images, then run:

```sh
python3 parsarium.py fandango setup
python3 scripts/smoke_fandango_defaults.py runs/fandango-default-smoke
```

The script writes per-format Fandango, replay, and plan receipts plus a
combined `smoke.json`. It starts no campaign. Fanbase defaults fetch a live
registry; the recorded spec hashes identify this run but future defaults may
change upstream. Replay reports target process completion. Some fuzz entries
can swallow a parser error, so this smoke alone does not establish semantic
acceptance of every generated file. The base projects separately verify their
valid controls. The MP3 routes generate silent Layer III frames; see
[the plain MP3 decision](plain-mp3-decision.md).

The first isolated run lacked the managed macOS certificate bundle for four
Fanbase fetches; using the managed Fandango setup resolved it. A pre-existing
PNG/LodePNG AFL image ID did not match its receipt, so the final run used the
verified OpenCV target. WAV images had been removed locally; the selected
`dr_wav` base and AFL images were rebuilt and their receipts refreshed.

The two MP3 rows were rechecked on 17 November 2026 after the MP3 targets moved
to `projects/mp3/` (`--case mp3/c/mpv --case mp3/go/github_com_dmulholl_mp3lib`).
The default grammar is now chosen per MP3 target from its control. Both outputs
are byte-identical to the first run; the untagged row now uses the default case
`dmulholl/mp3lib`, because the plain go-mp3 project was removed in the merge.

The MP4 row was rechecked on 19 November 2026 after `mp4.fan` gained an
optional AAC audio track and iTunes metadata
(`--case mp4/cpp/exiv2`). The default route now passes `--max-nodes 2000`
with the bundled spec, because Fandango's default node budget yields only
audio-only files without metadata. The seed-7 output is a video-only file. The
local Exiv2 base and AFL++ images were rebuilt and their receipts refreshed
first; the AFL++ feedback edge count is unchanged. The Fandango executable
hash differs from the other rows because the managed environment's entry
script records its own install path.

The PDF row was rechecked on 19 November 2026 after `pdf.fan` gained one to
five pages, per-page or inherited MediaBoxes, optional `/Rotate` and optional
Info fields (`--case pdf/cpp/poppler`). The default route now passes
`--max-nodes 2000` with the bundled spec, because Fandango's default node
budget yields only one- and two-page files. The seed-7 output has four pages.
The local Poppler base image had been rebuilt and its AFL++ image removed, so
both receipts were refreshed first; the base control coverage (39 library
lines) and the AFL++ feedback edge count (953) are unchanged.

The SVG row was rechecked on 19 November 2026 after SVG moved from Fanbase's
`svg` spec to the local `svg.fan` (`--case svg/c/librsvg`). The default route
passes `--max-nodes 2000` with the bundled spec, because Fandango's default
node budget yields one to six top-level elements. The seed-7 output is a
128×4 file with a viewBox, two ellipses, a rect, a line and nested groups. The
local librsvg base image differed from its receipt, so `afl build` re-verified
it (2,949 library lines, unchanged) and the AFL++ image, which was missing,
was rebuilt; control feedback is 5,204 edges (5,214 before), with the valid
path still adding stable edges.

The ASCII PLY row was rechecked on 20 November 2026 after `ascii_ply.fan`
gained meshes of 3–60 vertices with 1–60 polygonal faces, optional normals,
RGB or RGBA, `double` coordinates, an optional `edge` element and point
clouds (`--case ascii_ply/c/assetkit`). The default route now passes
`--max-nodes 5000` with the bundled spec, because Fandango's default node
budget yields only a few vertices and faces. The seed-7 output has 13
vertices with normals, 46 faces and 12 edges. The local AssetKit base image
differed from its receipt and its AFL++ image was missing, so `afl build`
re-verified the base (525 library lines, unchanged) and rebuilt the overlay
(2,116 feedback edges, unchanged).

The two MP3 rows were rechecked on 20 November 2026 after tagged MP3 moved
from Fanbase's `mp3` spec to the local `mp3_tagged.fan` and `mp3_plain.fan`
started generating its audio (`--case mp3/c/mpv --case
mp3/go/github_com_dmulholl_mp3lib`). Both routes pass `--max-nodes 2000`. The
seed-7 tagged output has an ID3v2.3 tag, an ID3v1 trailer and seven MPEG-1
32 kHz frames; the plain output has 28 MPEG-2 22.05 kHz frames. The
`dmulholl/mp3lib` base and AFL++ images had been rebuilt for the RQ2 harness
change before this check.
