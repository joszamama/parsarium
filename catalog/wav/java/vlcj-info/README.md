# vlcj-info — WAV / Java

- **Pinned release:** `2.0.3`
- **License:** GPL-3.0-or-later
- **Parsed scope:** WAV format, sample rate and channels
- **Underlying family:** vlcj-info JNA binding to libmediainfo
- **Local input API:** `new MediaInfoFile(String localWav).open(), info(String MediaInfo template)`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/uk/co/caprica/vlcj-info/2.0.3/vlcj-info-2.0.3-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/wav/parsers.json) · [control verification](../../../../data/java/wav/verification.json) · [within-ecosystem ranking](../../../../data/java/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "format": "Wave",
  "sample_rate": 8000,
  "channels": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/java/vlcj_info/README.md)

```sh
python3 parsarium.py build wav java vlcj_info
python3 parsarium.py run wav java vlcj_info controls/wav/256-samples.wav
```
