# sdl_mixer — MP3 with ID3v2 / C++

Pinned release: `2.8.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/cpp/sdl-mixer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 cpp sdl_mixer
python3 parsarium.py run mp3_id3v2 cpp sdl_mixer controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 cpp sdl_mixer CORPUS_DIR runs/mp3_id3v2-sdl_mixer-replay
python3 parsarium.py afl build mp3_id3v2 cpp sdl_mixer
python3 parsarium.py afl prepare mp3_id3v2 cpp sdl_mixer runs/mp3_id3v2-sdl_mixer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
