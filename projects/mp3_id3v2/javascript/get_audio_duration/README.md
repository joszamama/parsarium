# get-audio-duration — MP3 with ID3v2 / JavaScript

Pinned release: `4.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/javascript/get-audio-duration/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 javascript get_audio_duration
python3 parsarium.py run mp3_id3v2 javascript get_audio_duration controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 javascript get_audio_duration CORPUS_DIR runs/mp3_id3v2-get_audio_duration-replay
python3 parsarium.py afl build mp3_id3v2 javascript get_audio_duration
python3 parsarium.py afl prepare mp3_id3v2 javascript get_audio_duration runs/mp3_id3v2-get_audio_duration-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
