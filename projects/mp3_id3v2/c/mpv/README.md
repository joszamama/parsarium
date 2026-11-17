# mpv — MP3 with ID3v2 / C

Pinned release: `0.42.0`. [Manifest](manifest.json) · verification receipt: not yet recorded

[API, control result, and parser family](../../../../catalog/mp3_id3v2/c/mpv/README.md)

The harness writes the input to a local `.mp3` file and loads it through libmpv (`loadfile`, then `MPV_EVENT_FILE_LOADED`). It reads the title, the first track's codec and the duration. The valid control should report title `Parsarium`, codec `mp3` and 1000 ms.

mpv has no ID3v2 parser of its own. `demux/demux_lavf.c` hands the bytes to FFmpeg, where `avformat_open_input` reads the tag with `libavformat/id3v2.c` and `mp3dec.c` parses the MPEG audio frames. The image builds mpv 0.42.0, FFmpeg 9.0.2 and libplacebo 7.387.0 from pinned source with the same instrumentation. Coverage covers mpv's demuxer layer and FFmpeg `libavformat`. FFmpeg is built with `mp3` as its only demuxer.

This is the same `id3v2.c` and `mp3dec.c` that the direct [FFmpeg row](../ffmpeg/README.md) exercises, and the same libmpv that the C++ mpv catalog row calls.

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 c mpv
python3 parsarium.py run mp3_id3v2 c mpv controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 c mpv CORPUS_DIR runs/mp3_id3v2-mpv-replay
python3 parsarium.py afl build mp3_id3v2 c mpv
python3 parsarium.py afl prepare mp3_id3v2 c mpv runs/mp3_id3v2-mpv-afl
```

Replace `CORPUS_DIR` with a directory of matching files.

The AFL++ overlay runs the same `build.sh` with `PARSARIUM_BUILD=afl`. Its allowlist instruments only FFmpeg's `id3v2.c`, `id3v1.c`, `mp3dec.c`, the helpers `mp3dec.c` calls (`replaygain.c`, `libavcodec/mpegaudiodecheader.c`, `libavcodec/mpegaudio_parser.c`) and mpv's `demux/demux_lavf.c`. The build fails if any other archive member or the harness carries AFL++ guards.

`afl build` runs [build.py](../../../../fuzzing/afl-native/mp3_id3v2/c/mpv/build.py). It checks the guarded archive members and the exact output of the control and of `controls/mp3_id3v2/tone-tags-v24.mp3`, a second valid file with the same audio frames under an ID3v2.4 tag. Both must give identical AFL++ maps on every repeat, and the variant must add edges. The verified coverage image then replays both files, and the variant must reach `id3v2.c` regions the control does not. The AFL++ prepare command sets up a seeded run; it does not start a campaign.
