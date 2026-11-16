# codememory/media-file-fork — MP3 with ID3v2 / PHP

- **Pinned release:** `v1.0`
- **License:** MIT
- **Parsed scope:** MP3 audio type, 8 kHz sample rate, and 32 kb/s bit rate on an ID3v2.3-tagged control
- **Underlying family:** Mp3Info native MP3 and ID3v2 parser
- **Local input API:** `wapmorgan\MediaFile\MediaFile::open(local tagged MP3 path); isAudio and getAudio sample rate/bit rate`
- **Documentation:** [API reference](<https://github.com/codememory1/MediaFile/blob/affc235bb20d3fddb16ddc88821b5bf35c96af04/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp3_id3v2/parsers.json) · [control verification](../../../../data/php/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/php/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "is_audio": true,
  "sample_rate": 8000,
  "bit_rate": 32000
}
```

Fork of MediaFile; its pinned lock still delegates MP3 parsing to wapmorgan/mp3info. This API exposes MP3 audio properties rather than tag text.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/php/codememory_media_file_fork/README.md)

```sh
python3 parsarium.py build mp3_id3v2 php codememory_media_file_fork
python3 parsarium.py run mp3_id3v2 php codememory_media_file_fork controls/mp3_id3v2/tone-tags.mp3
```
