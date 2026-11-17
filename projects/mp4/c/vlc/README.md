# VLC — MP4 / C

Pinned release: `3.0.24`. The C harness writes input bytes to a private local file, opens it with `libvlc_media_new_path`, and parses it with `libvlc_media_parse_with_options`. The valid control reports title `Parsarium`, one H.264 video track, one AAC audio track, 2 × 2 video size, and 1000 ms duration.

The [Docker receipt](verification.json) records 2,046 executed lines in VLC's own MP4 demuxer, including 1,152 in its box parser. The build links only VLC's file access and MP4 demuxer plugins; no other demuxer is available. See the [manifest](manifest.json) and [AFL++ receipt](../../../../fuzzing/afl-native/mp4/c/vlc/verification.json).

```sh
python3 parsarium.py build mp4 c vlc
python3 parsarium.py run mp4 c vlc controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 c vlc CORPUS_DIR runs/vlc-mp4-replay
python3 parsarium.py afl build mp4 c vlc
python3 fuzzing/afl-native/mp4/c/vlc/verify_valid_variant.py
python3 parsarium.py afl prepare mp4 c vlc runs/vlc-mp4-afl
python3 parsarium.py afl run runs/vlc-mp4-afl --check
```

The AFL++ image instruments VLC as well as the harness. Its valid control produced 1,915 feedback edges. A second valid 3-second MP4 added [82 executed VLC MP4 parser regions and 43 stable AFL++ edges](../../../../fuzzing/afl-native/mp4/c/vlc/valid-variant.json) across three fixed-input probes. The C++ VLC entry point, when present, uses the same underlying MP4 demuxer family.
