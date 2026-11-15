# jaffree — MP3 with ID3v2 / Java

- **Pinned release:** `2024.08.29`
- **License:** Apache-2.0
- **Parsed scope:** local tagged MP3 codec, sample rate, title and artist
- **Underlying family:** Jaffree wrapper over local FFprobe/FFmpeg
- **Local input API:** `FFprobe.atPath(Path localBin).setShowStreams(true).setShowFormat(true).setInput(Path localMp3).execute()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/github/kokorin/jaffree/jaffree/2024.08.29/jaffree-2024.08.29-sources.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp3_id3v2/parsers.json) · [control verification](../../../../data/java/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/java/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "codec": "mp3",
  "frequency": 8000,
  "title": "Parsarium",
  "artist": "Control"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
