# mpv — MP3 with ID3v2 / C++

Pinned release: `0.42.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/cpp/mpv/README.md)

The C++17 harness writes the input to a local `.mp3` file, loads it with `mpv_command(loadfile)`, waits for `MPV_EVENT_FILE_LOADED`, then reads `metadata/by-key/title`, the first track's codec and `duration`. The control must return title `Parsarium`, codec `mp3` and 1000 ms.

mpv has no ID3v2 parser of its own. `demux/demux_lavf.c` hands the file to FFmpeg, where `avformat_open_input` reads the tag with `libavformat/id3v2.c` and `mp3dec.c` parses the MPEG audio frames. The image builds mpv 0.42.0, FFmpeg 9.0.2 and libplacebo 7.387.0 from pinned source with the same instrumentation. FFmpeg is built with `mp3` as its only demuxer. Coverage covers mpv's demuxer layer and FFmpeg `libavformat`.

The image also loads [`valid-v24.mp3`](valid-v24.mp3), a copy of `controls/mp3_id3v2/tone-tags-v24.mp3`: the same audio frames under an ID3v2.4 tag. It must give the same result, and the control check fails unless it reaches `id3v2.c` regions the control does not.

The AFL++ overlay instruments only FFmpeg's `id3v2.c`, `id3v1.c`, `mp3dec.c`, the helpers `mp3dec.c` calls (`replaygain.c`, `libavcodec/mpegaudiodecheader.c`, `libavcodec/mpegaudio_parser.c`) and mpv's `demux_lavf.c`. The build fails if guards land anywhere else, including the C++ harness. [build.py](../../../../fuzzing/afl-native/mp3_id3v2/cpp/mpv/build.py) checks the exact output of both files, requires identical maps on every repeat, and requires the ID3v2.4 file to add edges.

This row shares its parser with the C mpv row (`projects/mp3_id3v2/c/mpv`): same archives, same build, only the call site differs. The [C](../../c/ffmpeg/README.md) and [C++](../ffmpeg/README.md) FFmpeg rows parse with the same `id3v2.c` and `mp3dec.c` directly. It is not an independent parser.

In the AFL++ image, mpv's upstream fuzzing build accepts input only on file descriptor 42. The harness duplicates the local input there and calls `loadfile fd://42`; the pinned format demuxer and property checks are the same. Track decoding is disabled, while demuxed track metadata remains observable.

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 cpp mpv
python3 parsarium.py run mp3_id3v2 cpp mpv controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 cpp mpv CORPUS_DIR runs/mp3_id3v2-mpv-replay
python3 parsarium.py afl build mp3_id3v2 cpp mpv
python3 parsarium.py afl prepare mp3_id3v2 cpp mpv runs/mp3_id3v2-mpv-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
