# tika-mp4 — MP4 / Java

- **Pinned release:** `4.2.0`
- **License:** Apache-2.0
- **Parsed scope:** parsed video dimensions, audio properties and title
- **Underlying family:** Apache Tika MP4Parser over metadata-extractor
- **Local input API:** `MP4Parser.parse(TikaInputStream localMp4,ContentHandler,Metadata,ParseContext)`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-audiovideo-module/4.2.0/tika-parser-audiovideo-module-4.2.0-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/mp4/parsers.json) · [control verification](../../../../data/java/mp4/verification.json) · [within-ecosystem ranking](../../../../data/java/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "width": 2,
  "height": 2,
  "sample_rate": 8000,
  "channels": 1,
  "title": "Parsarium"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
