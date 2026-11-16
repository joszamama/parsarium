# taglib — WAV / C++

- **Pinned release:** `2.3.2`
- **License:** LGPL-2.1-only OR MPL-1.1
- **Parsed scope:** WAV-aware structural/audio-property parsing; does not decode PCM samples
- **Underlying family:** TagLib C bindings over TagLib C++ RIFF/WAV parser
- **Local input API:** `taglib_file_new_type(local WAV path, TagLib_File_WAV); taglib_file_audioproperties; sample rate, channels and bitrate accessors`
- **Documentation:** [API reference](<https://github.com/taglib/taglib/blob/v2.3.2/bindings/c/tag_c.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/wav/parsers.json) · [control verification](../../../../data/cpp/wav/verification.json) · [within-ecosystem ranking](../../../../data/cpp/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "bitrate_kbps": 128
}
```

The C binding wraps TagLib C++ and uses its RIFF/WAV properties implementation; one package path, not a separate C parser engine. It reports WAV sample rate, channel count and bitrate, not decoded samples. The C++ path uses the exact C-cell release and underlying decoder.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/cpp/taglib/README.md)

```sh
python3 parsarium.py build wav cpp taglib
python3 parsarium.py run wav cpp taglib controls/wav/four-samples.wav
```
