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
| SVG | `c/librsvg` | Fanbase `svg` | 1/1 / ready |
| HTTP/1.1 | `cpp/poco` | local `http11_request.fan` | 1/1 / ready |
| ASCII PLY | `c/assetkit` | local `ascii_ply.fan` | 1/1 / ready |
| ASCII PNM | `cpp/openimageio` | local `ascii_pnm_p3.fan` | 1/1 / ready |
| MP3, ID3v2-tagged control | `c/mpv` | Fanbase `mp3` | 1/1 / ready |
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
valid controls. The plain MP3 route is a [bounded valid-frame seed
generator](plain-mp3-decision.md), not a general MP3 grammar.

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
