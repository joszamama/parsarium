# juce — SVG / C++

Pinned release: `9.0.5` (AGPL-3.0-only). [Manifest](manifest.json) · [source lock](source-lock.json) · [Docker receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/svg/cpp/juce/verification.json)

[API, control result, and parser family](../../../../catalog/svg/cpp/juce/README.md)

The harness writes each input to a temporary local SVG, then calls `juce::Drawable::createFromSVGFile(juce::File(path))` and `getDrawableBounds()`. Inputs are capped at 1 MiB. The build compiles only the `juce_core`, `juce_events`, and `juce_graphics` module sources from the pinned JUCE release with clang and LLVM coverage. It uses no GUI module, no display, and no juceaide; WebP, fontconfig, and curl are off. The Docker build checks the source archive SHA-256 and the license, `juce_graphics` unity file, Drawable, SVG frontend, and bundled LunaSVG source files against the [source lock](source-lock.json). The control gate requires LLVM source coverage in `juce_SVGParser.cpp`, `juce_DrawableComposite.cpp`, and the bundled LunaSVG `svgparser.cpp` and `lunasvg.cpp`. It also checks that a valid 1×1 SVG ([`one-pixel.svg`](one-pixel.svg)) reports `{"width":1,"height":1}`.

JUCE's SVG frontend parses with a vendored copy of LunaSVG 3.5.0 and converts the result to a JUCE Drawable tree. It shares the LunaSVG parser family with the direct [LunaSVG row](../lunasvg/README.md).

The control returns the catalog result, `{"width":2,"height":1}`; a valid 1×1 SVG also parses. Docker replay covered 1,353 JUCE source lines, including the bundled LunaSVG parser. JUCE parses SVG into a Drawable tree and does not rasterize it, so the result has no pixel colors. The AFL++ overlay compiles the same JUCE module sources with AFL instrumentation and reported 814 edges on the control; repeat maps matched, and a valid red/blue SVG changed 94 edge IDs. The base image's libFuzzer binary has harness feedback only; use the AFL++ overlay for parser steering.

## Run from the repository root

```sh
python3 parsarium.py build svg cpp juce
python3 parsarium.py run svg cpp juce controls/svg/red-green.svg
python3 parsarium.py replay svg cpp juce CORPUS_DIR runs/svg-juce-replay
python3 parsarium.py afl build svg cpp juce
python3 parsarium.py afl prepare svg cpp juce runs/svg-juce-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
