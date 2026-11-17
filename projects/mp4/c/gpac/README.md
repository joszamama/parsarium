# gpac — MP4 / C

Pinned release: `26.07.0`. [Manifest](manifest.json) · [Docker receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/mp4/c/gpac/verification.json)

[API, control result, and parser family](../../../../catalog/mp4/c/gpac/README.md)

The valid two-track MP4 control passed Docker replay and one-case fuzzer smoke. A separate sample-free video-only MP4 also parses, reporting one video track and zero dimensions where no sample description is available. LLVM coverage reached 2,421 lines in the pinned GPAC ISO media parser. The AFL++ build reported 2,376 feedback edges on the control.

## Run from the repository root

```sh
python3 parsarium.py build mp4 c gpac
python3 parsarium.py run mp4 c gpac controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 c gpac CORPUS_DIR runs/mp4-gpac-replay
python3 parsarium.py afl build mp4 c gpac
python3 parsarium.py afl prepare mp4 c gpac runs/mp4-gpac-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Build profile:** libgpac is built statically from the pinned source with `--isomedia-only`. Its Linux build also disables the unrelated DVB filter and embedded documentation; the pinned release's DVB filter fails to compile against its own filter-register structure. Upstream configure ignores `--use-FOO=no` in this mode, so the image installs only zlib headers and no other optional libraries are detected. The harness writes each input to a temporary file and opens it with `gf_isom_open(..., GF_ISOM_OPEN_READ, NULL)`, the same public call as the catalog adapter. The source archive remains unchanged.
