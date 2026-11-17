# thorvg — SVG / C

Pinned release: `1.1.3`. [Manifest](manifest.json) · [Docker receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/svg/c/thorvg/verification.json)

[API, control result, and parser family](../../../../catalog/svg/c/thorvg/README.md)

The harness loads input bytes with `tvg_picture_load_data(..., "svg", NULL, true)`, reads `tvg_picture_get_size`, and renders through `tvg_swcanvas_create` into an `ARGB8888S` buffer. Its JSON output reports the decoded width and height, matching the catalog adapter; a valid 1×1 SVG is also accepted. ThorVG is built with Meson using only the CPU engine, the SVG loader, and the C API binding.

The valid 2×1 SVG control passed Docker replay and one-case fuzzer smoke, covering 2,476 ThorVG source lines. The source-built AFL++ overlay reported 2,057 edges on that control; repeated maps matched and a separate valid red/blue SVG changed 358 edge IDs. ThorVG's pinned global `new` uses `malloc`, so AddressSanitizer's allocation/deallocation mismatch check is disabled for the fuzzer startup. ASan's memory checks and UBSan remain enabled; this exception is bound in the manifest.

## Run from the repository root

```sh
python3 parsarium.py build svg c thorvg
python3 parsarium.py run svg c thorvg controls/svg/red-green.svg
python3 parsarium.py replay svg c thorvg CORPUS_DIR runs/svg-thorvg-replay
python3 parsarium.py afl build svg c thorvg
python3 parsarium.py afl prepare svg c thorvg runs/svg-thorvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
