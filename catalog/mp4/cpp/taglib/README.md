# taglib — MP4 / C++

- **Pinned release:** `2.3.2`
- **License:** LGPL-2.1-only OR MPL-1.1
- **Parsed scope:** MP4 title metadata and one-second duration
- **Underlying family:** TagLib native MP4 metadata parser
- **Local input API:** `TagLib::MP4::File(local MP4 filename); tag()->title(); audioProperties()->lengthInSeconds()`
- **Documentation:** [API reference](<https://taglib.org/api/>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp4/parsers.json) · [control verification](../../../../data/cpp/mp4/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium",
  "duration_seconds": 1
}
```

C binding delegates to the same TagLib C++ MP4 parser used by the C++ adapter.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/cpp/taglib/README.md)

```sh
python3 parsarium.py build mp4 cpp taglib
python3 parsarium.py run mp4 cpp taglib controls/mp4/red-av.mp4
```
