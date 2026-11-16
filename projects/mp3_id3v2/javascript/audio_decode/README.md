# @audio/decode — MP3 with ID3v2 / JavaScript

Pinned release: `4.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/javascript/audio-decode/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 javascript audio_decode
python3 parsarium.py run mp3_id3v2 javascript audio_decode controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 javascript audio_decode CORPUS_DIR runs/mp3_id3v2-audio_decode-replay
python3 parsarium.py afl build mp3_id3v2 javascript audio_decode
python3 parsarium.py afl prepare mp3_id3v2 javascript audio_decode runs/mp3_id3v2-audio_decode-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
