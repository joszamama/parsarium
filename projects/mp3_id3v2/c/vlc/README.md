# VLC — MP3 with ID3v2 / C

Pinned release: VLC `3.0.24` with TagLib `1.13.1` and VLC's two contrib patches. The C harness writes bytes to a private local `.mp3` file, then calls `libvlc_media_new_path` and `libvlc_media_parse_with_options`. The valid control reports title `Parsarium`, one MP3 track, 8000 Hz mono.

The [Docker receipt](verification.json) confirms two ID3v2 readers on this route. VLC's `skiptags` filter and MPEG audio demuxer reach its own ID3v2 source, then VLC's TagLib meta reader reparses the file with TagLib; its title wins. The control covers 39 VLC ID3 tag lines, 53 VLC ID3 frame lines, 109 TagLib ID3 tag lines, and 96 TagLib ID3 frame lines. Only the five required plugins are linked. See the [manifest](manifest.json) and [AFL++ receipt](../../../../fuzzing/afl-native/mp3_id3v2/c/vlc/verification.json).

```sh
python3 parsarium.py build mp3_id3v2 c vlc
python3 parsarium.py run mp3_id3v2 c vlc controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 c vlc CORPUS_DIR runs/vlc-mp3-replay
python3 parsarium.py afl build mp3_id3v2 c vlc
python3 fuzzing/afl-native/mp3_id3v2/c/vlc/verify_valid_variant.py
python3 parsarium.py afl prepare mp3_id3v2 c vlc runs/vlc-mp3-afl
python3 parsarium.py afl run runs/vlc-mp3-afl --check
```

The AFL++ control produced 2,391 edges. A [second valid ID3v2.4 file](../../../../fuzzing/afl-native/mp3_id3v2/c/vlc/valid-variant.json) reached five additional VLC ID3v2 regions and 16 additional TagLib ID3v2 regions, adding 30 stable AFL++ edges. The file has the same audio frames as the ID3v2.3 control. The C++ VLC entry point shares this parser family.
