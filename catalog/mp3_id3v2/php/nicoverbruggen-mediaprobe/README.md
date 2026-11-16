# nicoverbruggen/mediaprobe — MP3 with ID3v2 / PHP

- **Pinned release:** `v1.1`
- **License:** MIT
- **Parsed scope:** ID3v2.3 title, artist, and album through FFprobe
- **Underlying family:** FFmpeg native MP3 and ID3 parser
- **Local input API:** `MediaProbe(local tagged MP3 path)::getMediaInfo(); format.tags title/artist/album`
- **Documentation:** [API reference](<https://github.com/nicoverbruggen/mediaprobe/blob/aa824d0691598dc9d66301f78da2687bc656884c/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp3_id3v2/parsers.json) · [control verification](../../../../data/php/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/php/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot"
}
```

Composer wrapper delegates to local FFprobe 9.0.2; package path over the FFmpeg parser family, not an independent decoder.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/php/nicoverbruggen_mediaprobe/README.md)

```sh
python3 parsarium.py build mp3_id3v2 php nicoverbruggen_mediaprobe
python3 parsarium.py run mp3_id3v2 php nicoverbruggen_mediaprobe controls/mp3_id3v2/tone-tags.mp3
```
