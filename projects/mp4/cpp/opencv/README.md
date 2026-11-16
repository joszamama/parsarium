# opencv — MP4 / C++

Pinned release: `5.1.0`. [Manifest](manifest.json)

[API, control result, and parser family](../../../../catalog/mp4/cpp/opencv/README.md)

The harness accepts inputs up to 1 MiB whose first box is `ftyp`, writes them to a temporary `.mp4` file, opens it with `cv::VideoCapture(path, cv::CAP_FFMPEG)` and reports `CAP_PROP_FRAME_WIDTH`, `CAP_PROP_FRAME_HEIGHT`, `CAP_PROP_FRAME_COUNT` and `CAP_PROP_FPS`, rounded like the catalog adapter. OpenCV is a wrapper here: its videoio FFmpeg backend (`cap_ffmpeg_impl.hpp`) hands the file to the FFmpeg MOV/MP4 demuxer (`libavformat/mov.c`) and the H.264 decoder.

Both packages are built from pinned release tarballs: OpenCV 5.1.0 and FFmpeg 9.0.2, the FFmpeg release the catalog's Homebrew OpenCV linked. FFmpeg is configured with only the file protocol, the mov demuxer, H.264 and AAC decoders and parsers, libswscale and zlib, without threads. OpenCV builds core, flann, geometry, imgproc, imgcodecs and videoio, with FFmpeg as the only video backend and every image codec off. FFmpeg and OpenCV get the same LLVM coverage, sanitizer and fuzzer instrumentation, so coverage, libFuzzer and the AFL++ overlay observe the FFmpeg demuxer and not only the OpenCV wrapper.

The pinned 2×2 MP4 control passed Docker replay and one-case fuzzer smoke. The replay covered 567 OpenCV videoio lines and 3,911 underlying FFmpeg lines, including the MOV/MP4 demuxer. The AFL++ overlay reported 11,391 feedback edges on the same control. [Docker receipt](verification.json) and [AFL++ receipt](../../../../fuzzing/afl-native/mp4/cpp/opencv/verification.json) record the images, input hash, and toolchain.

## Run from the repository root

```sh
python3 parsarium.py build mp4 cpp opencv
python3 parsarium.py run mp4 cpp opencv controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 cpp opencv CORPUS_DIR runs/mp4-opencv-replay
python3 parsarium.py afl build mp4 cpp opencv
python3 parsarium.py afl prepare mp4 cpp opencv runs/mp4-opencv-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
