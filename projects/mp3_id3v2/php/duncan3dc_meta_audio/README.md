# duncan3dc/meta-audio — MP3 with ID3v2 / PHP

Pinned release: `0.6.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/php/duncan3dc-meta-audio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 php duncan3dc_meta_audio
python3 parsarium.py run mp3_id3v2 php duncan3dc_meta_audio controls/mp3_id3v2/tone-tags-v24.mp3
python3 parsarium.py replay mp3_id3v2 php duncan3dc_meta_audio CORPUS_DIR runs/mp3_id3v2-duncan3dc_meta_audio-replay
python3 parsarium.py afl build mp3_id3v2 php duncan3dc_meta_audio
python3 parsarium.py afl prepare mp3_id3v2 php duncan3dc_meta_audio runs/mp3_id3v2-duncan3dc_meta_audio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
