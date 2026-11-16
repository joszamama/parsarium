# exiv2 — MP4 / C++

Pinned release: `0.28.9`. [Manifest](manifest.json) · [source lock](source-lock.json)

[API, control result, and parser family](../../../../catalog/mp4/cpp/exiv2/README.md)

The harness writes the input bytes to a temporary `.mp4` file and calls `Exiv2::ImageFactory::open(path)`, `Image::readMetadata()` and `XmpData::findKey` for `Xmp.video.MajorBrand`, `Xmp.video.Width` and `Xmp.video.Height`. It accepts the file only when Exiv2 selects its native QuickTime reader (`src/quicktimevideo.cpp`). Exiv2 labels the `isom` brand `MP4 Base Media v1 [IS0 14496-12:2003]`; the harness reports the name without the version suffix. This is Exiv2's own parser, not FFmpeg or TagLib.

Exiv2 is built as a minimal static library with video support on and the XMP SDK, PNG, BMFF, Brotli, NLS, inih, WebReady and LensData off. Inputs over 1 MiB are rejected.

The pinned MP4 control passed Docker replay and one-case fuzzer smoke. It covered 1,375 Exiv2 source lines, including 597 lines in `quicktimevideo.cpp`. The AFL++ overlay rebuilt Exiv2 with feedback instrumentation and observed 2,360 edges on the same control. See the [Docker receipt](verification.json) and [AFL++ receipt](../../../../fuzzing/afl-native/mp4/cpp/exiv2/verification.json).

## Run from the repository root

```sh
python3 parsarium.py build mp4 cpp exiv2
python3 parsarium.py run mp4 cpp exiv2 controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 cpp exiv2 CORPUS_DIR runs/mp4-exiv2-replay
python3 parsarium.py afl build mp4 cpp exiv2
python3 parsarium.py afl prepare mp4 cpp exiv2 runs/mp4-exiv2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
