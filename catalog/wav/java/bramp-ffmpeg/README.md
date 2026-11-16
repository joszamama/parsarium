# bramp-ffmpeg — WAV / Java

- **Pinned release:** `0.9.2`
- **License:** BSD-2-Clause
- **Parsed scope:** WAV format, PCM codec, sample rate and channels
- **Underlying family:** bramp FFprobe CLI wrapper over FFmpeg
- **Local input API:** `new FFprobe(String localExecutable).probe(String localWav).getStreams()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/net/bramp/ffmpeg/ffmpeg/0.9.2/ffmpeg-0.9.2-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/wav/parsers.json) · [control verification](../../../../data/java/wav/verification.json) · [within-ecosystem ranking](../../../../data/java/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "format": "wav",
  "codec": "pcm_s16le",
  "sample_rate": 8000,
  "channels": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/java/bramp_ffmpeg/README.md)

```sh
python3 parsarium.py build wav java bramp_ffmpeg
python3 parsarium.py run wav java bramp_ffmpeg controls/wav/256-samples.wav
```
