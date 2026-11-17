# VLC — MP3 with ID3v2 / C++

VLC `3.0.24` and its patched TagLib `1.13.1` are built from pinned source. The C++17 harness writes input bytes to a private local `.mp3`, calls `libvlc_media_new_path()` and `libvlc_media_parse_with_options()`, then reports the title and audio stream metadata. [Manifest](manifest.json) · [control receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/mp3_id3v2/cpp/vlc/verification.json)

The valid ID3v2.3 control reports `Parsarium`, one MP3 audio track at 8000 Hz, mono. Source coverage reaches 293 lines in VLC's metadata reader and 377 lines in TagLib's MPEG/ID3v2 parser. A second valid ID3v2.4 file takes different ID3 text and frame paths. The AFL++ build restricts feedback to TagLib and VLC's MP3/ID3v2 modules: 640 stable control edges, with 23 edges exclusive to the valid v2.4 file across three probes. [Catalog evidence and shared family](../../../../catalog/mp3_id3v2/cpp/vlc/README.md).

From the repository root:

```sh
python3 parsarium.py build mp3_id3v2 cpp vlc
python3 parsarium.py run mp3_id3v2 cpp vlc controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py afl build mp3_id3v2 cpp vlc
python3 parsarium.py afl prepare mp3_id3v2 cpp vlc runs/vlc-cpp-mp3
python3 parsarium.py afl run runs/vlc-cpp-mp3 --check
```

The input limit is 1 MiB. AFL preparation creates a seeded run; `--check` validates it without starting a campaign. The C and C++ VLC paths share the same underlying parser family.
