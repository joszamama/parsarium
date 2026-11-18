# taglib — MP4 / C

- **Pinned release:** `2.3.2`
- **Upstream:** [source repository](<https://github.com/taglib/taglib>) · [Debian](<https://tracker.debian.org/pkg/taglib>)
- **License:** LGPL-2.1-only OR MPL-1.1
- **Parsed scope:** MP4 title metadata and one-second duration
- **Underlying family:** TagLib native MP4 metadata parser
- **Local input API:** `taglib_file_new(local MP4 filename); taglib_file_tag; taglib_tag_title; taglib_file_audioproperties`
- **Documentation:** [API reference](<https://github.com/taglib/taglib/blob/v2.3.2/bindings/c/tag_c.h>)
- **Catalog evidence:** [parser record](../../../../data/c/mp4/parsers.json) · [control verification](../../../../data/c/mp4/verification.json) · [within-ecosystem ranking](../../../../data/c/mp4/ranking.md)
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

[Docker harness and verification receipt](../../../../projects/mp4/c/taglib/README.md)

```sh
python3 parsarium.py build mp4 c taglib
python3 parsarium.py run mp4 c taglib controls/mp4/red-av.mp4
```
