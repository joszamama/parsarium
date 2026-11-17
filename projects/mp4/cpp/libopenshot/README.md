# libopenshot — MP4 / C++

Pinned release: `1.1.1`, built with libopenshot-audio `1.0.2` and FFmpeg `9.0.2`. [Manifest](manifest.json) · [control receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/mp4/cpp/libopenshot/verification.json)

[API, control result, and parser family](../../../../catalog/mp4/cpp/libopenshot/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 cpp libopenshot
python3 parsarium.py run mp4 cpp libopenshot controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 cpp libopenshot CORPUS_DIR runs/mp4-libopenshot-replay
python3 parsarium.py afl build mp4 cpp libopenshot
python3 parsarium.py afl prepare mp4 cpp libopenshot runs/mp4-libopenshot-afl
python3 parsarium.py afl run runs/mp4-libopenshot-afl --check
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

The harness writes the input to a temporary `.mp4`, constructs `openshot::FFmpegReader(path, false)`, and calls `Open()` once. It reports `has_video`, `has_audio`, `width`, `height`, `vcodec`, and `acodec` from `ReaderInfo`. An `openshot::ExceptionBase` counts as a rejected input. Any other exception is a crash.

**Coverage:** the valid control reaches 491 lines in libopenshot's `FFmpegReader.cpp` and 1,795 lines in FFmpeg's `mov.c`. The AFL++ build limits feedback to those two files: 1,145 control edges, stable across repeated runs, with one edge added by a second valid MP4. OpenShotAudio and Qt are not instrumented.

**Parser family:** `FFmpegReader` parses MP4 through libavformat's MOV/MP4 demuxer. It belongs to the same FFmpeg parser family as the FFmpeg, MLT, and other FFmpeg-backed targets, and does not count as an independent MP4 parser.

**Coverage limit:** the minimal FFmpeg build enables only the H.264 and AAC decoders. Inputs with other codecs fail to open, or have their audio stream disabled.

**Native engine limit:** the libFuzzer binary only passes a smoke test. Its libraries carry no sanitizer coverage, so in-process native fuzzing is unsupported. Use one-input replay or the prepared AFL++ run, which starts a fresh process per input.
