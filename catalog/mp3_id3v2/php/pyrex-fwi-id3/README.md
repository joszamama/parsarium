# pyrex-fwi/id3 — MP3 with ID3v2 / PHP

- **Pinned release:** `v0.2.0`
- **License:** MIT
- **Parsed scope:** ID3v2.3 title, artist, and album on an 18-second MP3
- **Underlying family:** MediaInfoLib native MP3 and ID3 parser
- **Local input API:** `Id3Metadata(local tagged MP3 path) passed to MediainfoWrapper::read; getTitle/getArtist/getAlbum`
- **Documentation:** [API reference](<https://github.com/Pyrex-FWI/id3/blob/3e51c7b10db82d6f3a7d18c7ea58cc481314ed8a/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp3_id3v2/parsers.json) · [control verification](../../../../data/php/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/php/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags-long.mp3`](../../../../controls/mp3_id3v2/tone-tags-long.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot"
}
```

Composer wrapper invokes MediaInfo 26.10. The committed executable shim changes its requested --Output=XML to --Output=OLDXML, matching the schema this pinned package expects; no parser output is fabricated.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
