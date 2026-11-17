# mpv — MP4 / C

Pinned release: `0.42.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/c/mpv/README.md)

The harness writes the input to a local `.mp4` file and loads it through libmpv (`loadfile`, then `MPV_EVENT_FILE_LOADED`). libmpv opens MP4 through `demux/demux_lavf.c`, which hands the bytes to FFmpeg's MOV/MP4 demuxer. The image builds mpv 0.42.0, FFmpeg 9.0.2 and libplacebo 7.387.0 from pinned source with the same instrumentation. Coverage covers mpv's demuxer layer and FFmpeg `libavformat`, where `mov.c` is the box parser. FFmpeg is built with `mov` as its only demuxer.

The AFL++ overlay builds the same sources with `PARSARIUM_BUILD=afl`. An `AFL_LLVM_ALLOWLIST` limits instrumentation to `mov.c`, the `isom.c`, `mov_chan.c` and `mov_esds.c` helpers, and mpv's `demux_lavf.c`. The build fails if guards land in any other archive member or in the C harness. The overlay check replays the control and [`red-av-3s.mp4`](../../../../controls/mp4/red-av-3s.mp4), a second valid MP4 with no title and `stss` and `ctts` boxes, and requires exact results for both. It also requires the second MP4 to add stable edges that no control probe reaches.

This is the same `mov.c` that the direct [FFmpeg row](../ffmpeg/README.md) exercises, and the same libmpv that the C++ mpv catalog row calls.

In the AFL++ image, mpv's upstream fuzzing build accepts input only on file descriptor 42. The harness duplicates the local input there and calls `loadfile fd://42`; the pinned format demuxer and property checks are the same. Track decoding is disabled, while demuxed track metadata remains observable.

## Run from the repository root

```sh
python3 parsarium.py build mp4 c mpv
python3 parsarium.py run mp4 c mpv controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 c mpv CORPUS_DIR runs/mp4-mpv-replay
python3 parsarium.py afl build mp4 c mpv
python3 parsarium.py afl prepare mp4 c mpv runs/mp4-mpv-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
