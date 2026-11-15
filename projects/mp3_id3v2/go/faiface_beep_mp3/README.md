# github.com/faiface/beep/mp3 — MP3 with ID3v2 / Go

Pinned release: `v1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/go/github-com-faiface-beep-mp3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 go faiface_beep_mp3
python3 parsarium.py run mp3_id3v2 go faiface_beep_mp3 controls/mp3_id3v2/tone-tags-44k.mp3
python3 parsarium.py replay mp3_id3v2 go faiface_beep_mp3 CORPUS_DIR runs/mp3_id3v2-faiface_beep_mp3-replay
python3 parsarium.py afl build mp3_id3v2 go faiface_beep_mp3
python3 parsarium.py afl prepare mp3_id3v2 go faiface_beep_mp3 runs/mp3_id3v2-faiface_beep_mp3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
