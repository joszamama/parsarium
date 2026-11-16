# mediainfo-jna-wrapper — WAV / Java

- **Pinned release:** `2.1.9`
- **License:** MIT + MediaInfoLib Binary License
- **Parsed scope:** WAV format, sample rate and channels
- **Underlying family:** amilesend JNA binding to libmediainfo
- **Local input API:** `new MediaInfo(new MediaInfoAccessor(MediaInfoLibrary.newInstance())).open(File localWav).get(StreamType.Audio,0,String)`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/amilesend/mediainfo-jna-wrapper/2.1.9/mediainfo-jna-wrapper-2.1.9-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/wav/parsers.json) · [control verification](../../../../data/java/wav/verification.json) · [within-ecosystem ranking](../../../../data/java/wav/ranking.md)
- **Valid control:** [`controls/wav/32768-samples.wav`](../../../../controls/wav/32768-samples.wav)

## Observed control result

```json
{
  "format": "Wave",
  "sample_rate": 8000,
  "channels": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/java/mediainfo_jna_wrapper/README.md)

```sh
python3 parsarium.py build wav java mediainfo_jna_wrapper
python3 parsarium.py run wav java mediainfo_jna_wrapper controls/wav/32768-samples.wav
```
