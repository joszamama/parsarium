# indiehd/audio-manipulator — MP3 / PHP

Pinned release: `v4.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/php/indiehd-audio-manipulator/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 php indiehd_audio_manipulator
python3 parsarium.py run mp3_id3v2 php indiehd_audio_manipulator controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 php indiehd_audio_manipulator CORPUS_DIR runs/mp3_id3v2-indiehd_audio_manipulator-replay
python3 parsarium.py afl build mp3_id3v2 php indiehd_audio_manipulator
python3 parsarium.py afl prepare mp3_id3v2 php indiehd_audio_manipulator runs/mp3_id3v2-indiehd_audio_manipulator-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
