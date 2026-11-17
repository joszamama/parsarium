# mpv — MP4 / C++

Pinned release: `0.42.0`. [Manifest](manifest.json) · verification receipt: not yet recorded

[API, control result, and parser family](../../../../catalog/mp4/cpp/mpv/README.md)

The C++17 harness writes the input to a local `.mp4` file, loads it with `mpv_command(loadfile)`, waits for `MPV_EVENT_FILE_LOADED`, then reads `file-format`, `metadata/by-key/title` and the first video and audio track codecs. libmpv opens MP4 through `demux/demux_lavf.c`, which hands the bytes to FFmpeg's MOV/MP4 demuxer. The image builds mpv 0.42.0, FFmpeg 9.0.2 and libplacebo 7.387.0 from pinned source with the same instrumentation. Coverage covers mpv's demuxer layer and FFmpeg `libavformat`, where `mov.c` is the box parser. FFmpeg is built with `mov` as its only demuxer.

The control must return the catalog result: container `mov,mp4,m4a,3gp,3g2,mj2`, title `Parsarium`, `h264` and `aac`. The image also loads [`valid-3s.mp4`](valid-3s.mp4), a copy of `controls/mp4/red-av-3s.mp4`: a second valid MP4 with no title and `stss` and `ctts` boxes that the control lacks. The control check fails unless `mov.c` reads those two boxes only for that file.

The AFL++ overlay instruments only `mov.c`, the `isom.c`, `mov_chan.c` and `mov_esds.c` helpers, and mpv's `demux_lavf.c`. The build fails if guards land anywhere else, including the C++ harness. The overlay check requires the second MP4 to add stable edges that no control probe reaches.

This row shares its parser with the [C mpv row](../../c/mpv/README.md): same archives, same build, only the call site differs. The [C](../../c/ffmpeg/README.md) and [C++](../ffmpeg/README.md) FFmpeg rows parse with the same `mov.c` directly. It is not an independent parser.

## Run from the repository root

```sh
python3 parsarium.py build mp4 cpp mpv
python3 parsarium.py run mp4 cpp mpv controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 cpp mpv CORPUS_DIR runs/mp4-mpv-replay
python3 parsarium.py afl build mp4 cpp mpv
python3 parsarium.py afl prepare mp4 cpp mpv runs/mp4-mpv-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
