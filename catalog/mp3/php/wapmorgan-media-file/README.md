# wapmorgan/media-file — MP3 / PHP

- **Pinned release:** `0.1.4`
- **Upstream:** [source repository](<https://github.com/wapmorgan/MediaFile>) · [Packagist](<https://packagist.org/packages/wapmorgan/media-file>)
- **License:** MIT
- **Parsed scope:** MP3 audio type, 8 kHz sample rate, and 32 kb/s bit rate on an ID3v2.3-tagged control
- **Underlying family:** Mp3Info native MP3 and ID3v2 parser
- **Local input API:** `MediaFile::open(local tagged MP3 path); isAudio and getAudio sample rate/bit rate`
- **Documentation:** [API reference](<https://github.com/wapmorgan/MediaFile/blob/263f773696e02d173fb9636c9a8111ac84032292/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp3/parsers.json) · [control verification](../../../../data/php/mp3/verification.json) · [within-ecosystem ranking](../../../../data/php/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "is_audio": true,
  "sample_rate": 8000,
  "bit_rate": 32000
}
```

MediaFile wraps the pinned wapmorgan/mp3info parser in its isolated lock. This adapter exposes audio properties, not the tag text; it is a separate package path, not an independent parser family.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/php/wapmorgan_media_file/README.md)

```sh
python3 parsarium.py build mp3 php wapmorgan_media_file
python3 parsarium.py run mp3 php wapmorgan_media_file controls/mp3/id3v2-tagged-tone.mp3
```
