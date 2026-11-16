# opencv — PNG / C++

Pinned release: `5.1.0`. [Manifest](manifest.json)

[API, control result, and parser family](../../../../catalog/png/cpp/opencv/README.md)

The harness writes the input to a temporary `.png` file, calls `cv::imread(path, cv::IMREAD_UNCHANGED)` and reports decoded dimensions. It also reports the first two pixels as RGBA when the decoded depth is 8-bit; absent samples are `null`. OpenCV's imgcodecs PNG decoder reads the chunks and hands them to libpng. Both come from the pinned OpenCV source tarball: the build uses its bundled libpng 1.6.57 and zlib 1.3.2, not Ubuntu packages. Only the core, flann, geometry, imgproc and imgcodecs modules are built, with every other codec and optional dependency off.

The macOS catalog run linked Homebrew libpng 1.6.59, so the libpng version here differs from the catalog record.

The pinned red/green PNG passed Docker replay and one-case fuzzer smoke. It covered 401 OpenCV imgcodecs source lines and 1,387 bundled libpng lines; the AFL++ overlay observed 1,939 feedback edges on the same control. A separate valid 1×1 RGBA PNG replay returned `{"width":1,"height":1,"first":[255,0,0,255],"second":null}`. See the [Docker receipt](verification.json) and [AFL++ receipt](../../../../fuzzing/afl-native/png/cpp/opencv/verification.json).

## Run from the repository root

```sh
python3 parsarium.py build png cpp opencv
python3 parsarium.py run png cpp opencv controls/png/red-green.png
python3 parsarium.py replay png cpp opencv CORPUS_DIR runs/png-opencv-replay
python3 parsarium.py afl build png cpp opencv
python3 parsarium.py afl prepare png cpp opencv runs/png-opencv-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
