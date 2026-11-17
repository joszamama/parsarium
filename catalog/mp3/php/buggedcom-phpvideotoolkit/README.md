# buggedcom/phpvideotoolkit — MP3 / PHP

- **Pinned release:** `2.2.5`
- **License:** MIT
- **Parsed scope:** ID3v2.3 text fields and MP3 audio codec/sample rate
- **Underlying family:** FFmpeg native MP3 and ID3 parser
- **Local input API:** `PHPVideoToolkit\MediaParser::getFileInformation(local tagged MP3 path); metadata title/artist/album and audio sample rate/codec`
- **Documentation:** [API reference](<https://github.com/buggedcom/phpvideotoolkit-v2/blob/383a5b2c0ee7f4de4efea9a9154bb693630bbe0f/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp3/parsers.json) · [control verification](../../../../data/php/mp3/verification.json) · [within-ecosystem ranking](../../../../data/php/mp3/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot",
  "sample_rate": 8000,
  "codec": "mp3"
}
```

Composer package delegates to the local FFmpeg/FFprobe backend; separate PHP wrapper package path, not an independent parser family. Pinned source LICENSE.md offers MIT, while composer.json also lists GPL-3.0+.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/php/buggedcom_phpvideotoolkit/README.md)

```sh
python3 parsarium.py build mp3 php buggedcom_phpvideotoolkit
python3 parsarium.py run mp3 php buggedcom_phpvideotoolkit controls/mp3_id3v2/tone-tags.mp3
```
