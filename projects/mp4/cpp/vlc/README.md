# VLC — MP4 / C++

Pinned release: `3.0.24`. The C++17 harness writes input bytes to a private local file, opens it with `libvlc_media_new_path`, and parses it with `libvlc_media_parse_with_options`. The valid control reports title `Parsarium`, one H.264 video track, one AAC audio track, 2 × 2 frames and 1000 ms duration.

The [Docker receipt](verification.json) records 2,046 executed lines in VLC's MP4 demuxer, including 1,152 in its box parser. Only VLC's file access and MP4 demuxer plugins are linked. A valid 3-second MP4 additionally reaches the `stss` and `ctts` box readers. This C++ call site shares the underlying parser family with [C VLC](../../c/vlc/). See the [manifest](manifest.json) and [AFL++ receipt](../../../../fuzzing/afl-native/mp4/cpp/vlc/verification.json).

```sh
python3 parsarium.py build mp4 cpp vlc
python3 parsarium.py run mp4 cpp vlc controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 cpp vlc CORPUS_DIR runs/vlc-cpp-mp4-replay
python3 parsarium.py afl build mp4 cpp vlc
python3 parsarium.py afl prepare mp4 cpp vlc runs/vlc-cpp-mp4-afl
python3 parsarium.py afl run runs/vlc-cpp-mp4-afl --check
```

The AFL++ overlay instruments only VLC's MP4 demuxer plugin sources. Its control produced 508 feedback edges with identical maps across three probes; the valid 3-second MP4 added 39 stable edges.
