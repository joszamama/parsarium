# tika-audiovideo — WAV / Java

- **Pinned release:** `4.2.0`
- **License:** Apache-2.0
- **Parsed scope:** WAV sample rate and channels in parsed metadata
- **Underlying family:** Apache Tika AudioParser over Java Sound SPI
- **Local input API:** `AudioParser.parse(TikaInputStream, ContentHandler, Metadata, ParseContext)`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-audiovideo-module/4.2.0/tika-parser-audiovideo-module-4.2.0-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/wav/parsers.json) · [control verification](../../../../data/java/wav/verification.json) · [within-ecosystem ranking](../../../../data/java/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
