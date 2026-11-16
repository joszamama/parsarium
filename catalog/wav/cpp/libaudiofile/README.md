# libaudiofile — WAV / C++

- **Pinned release:** `0.3.6`
- **License:** LGPL-2.1
- **Parsed scope:** WAV sample rate, channel and frame counts, plus first four decoded PCM samples
- **Underlying family:** Audio File Library WAV parser
- **Local input API:** `afOpenFile(local WAV path, "r"); afGetFileFormat(AF_FILE_WAVE); afSetVirtualSampleFormat; afReadFrames; afGetRate, afGetChannels, afGetFrameCount`
- **Documentation:** [API reference](<https://github.com/mpruett/audiofile/blob/audiofile-0.3.6/libaudiofile/audiofile.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/wav/parsers.json) · [control verification](../../../../data/cpp/wav/verification.json) · [within-ecosystem ranking](../../../../data/cpp/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "frames": 4,
  "samples": [
    0,
    1000,
    -1000,
    0
  ]
}
```

Tagged 0.3.6 C API from mpruett/audiofile, unrelated to the Conan audiofile recipe for a C++ header-only package. One build-only signed-shift compatibility patch is documented. The C++ path uses the exact C-cell release and underlying decoder.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/cpp/libaudiofile/README.md)

```sh
python3 parsarium.py build wav cpp libaudiofile
python3 parsarium.py run wav cpp libaudiofile controls/wav/four-samples.wav
```
