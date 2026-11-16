# codememory/media-file-fork — MP3 with ID3v2 / PHP

Pinned release: `v1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/php/codememory-media-file-fork/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 php codememory_media_file_fork
python3 parsarium.py run mp3_id3v2 php codememory_media_file_fork controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 php codememory_media_file_fork CORPUS_DIR runs/mp3_id3v2-codememory_media_file_fork-replay
python3 parsarium.py afl build mp3_id3v2 php codememory_media_file_fork
python3 parsarium.py afl prepare mp3_id3v2 php codememory_media_file_fork runs/mp3_id3v2-codememory_media_file_fork-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
