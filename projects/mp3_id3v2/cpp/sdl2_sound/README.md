# sdl2_sound — MP3 with ID3v2 / C++

Pinned release: `2.0.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/cpp/sdl2-sound/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 cpp sdl2_sound
python3 parsarium.py run mp3_id3v2 cpp sdl2_sound controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 cpp sdl2_sound CORPUS_DIR runs/mp3_id3v2-sdl2_sound-replay
python3 parsarium.py afl build mp3_id3v2 cpp sdl2_sound
python3 parsarium.py afl prepare mp3_id3v2 cpp sdl2_sound runs/mp3_id3v2-sdl2_sound-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
