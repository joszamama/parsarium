# QtSvg — SVG / C++

Pinned QtSvg and QtBase release: `6.12.0`. The [Qt API](https://doc.qt.io/qt-6/qsvgrenderer.html) accepts local SVG bytes through `QSvgRenderer::load(QByteArray)`. The harness renders to `QImage` and reports dimensions and the first and last pixels of the top row. For a one-pixel-wide SVG, `second` is `null`.

## Run from the repository root

```sh
python3 parsarium.py build svg cpp qtsvg
python3 parsarium.py run svg cpp qtsvg controls/svg/red-green.svg
python3 parsarium.py replay svg cpp qtsvg CORPUS_DIR runs/svg-qtsvg-replay
python3 parsarium.py afl build svg cpp qtsvg
python3 parsarium.py afl prepare svg cpp qtsvg runs/svg-qtsvg-afl
```

Replace `CORPUS_DIR` with a directory of SVG inputs. The AFL++ command prepares a seeded run; it does not start a campaign. See the [manifest](manifest.json), [control receipt](verification.json), and [catalog record](../../../../catalog/svg/cpp/qtsvg/README.md).

The valid red/green control covers 1,044 QtSvg source lines, including 542 in `qsvghandler.cpp`. The [AFL++ overlay](../../../../fuzzing/afl-native/svg/cpp/qtsvg/verification.json) records 704 feedback edges. A [valid-input feedback check](../../../../fuzzing/afl-native/svg/cpp/qtsvg/valid-feedback.json) confirms an identical repeated map and 35 different edge IDs for a second valid SVG. Reproduce that check with `python3 fuzzing/afl-native/svg/cpp/qtsvg/verify-valid-feedback.py` after building the AFL++ image.
