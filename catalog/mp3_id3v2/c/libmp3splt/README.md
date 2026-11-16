# libmp3splt — MP3 with ID3v2 / C

- **Pinned release:** `0.9.2`
- **License:** GPL-2.0-or-later
- **Parsed scope:** MP3 frame-aware in-memory split of a 0.5-second segment from tagged local MP3; no ID3v2 text exposed
- **Underlying family:** libmp3splt MP3 plugin over libmad and libid3tag
- **Local input API:** `mp3splt_set_filename_to_split(local filename); mp3splt_append_splitpoint(0,50); mp3splt_split with SPLT_OPT_PRETEND_TO_SPLIT and write callback`
- **Documentation:** [API reference](<https://mp3splt.sourceforge.net/mp3splt_page/documentation/libmp3splt_api/mp3splt_8h.html>)
- **Catalog evidence:** [parser record](../../../../data/c/mp3_id3v2/parsers.json) · [control verification](../../../../data/c/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/c/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "split_status": 1,
  "segment_bytes": 2304,
  "frame_header": "ffe348c0"
}
```

libmp3splt uses its own frame-aware split API with a bundled MP3 plugin linked to libmad and libid3tag. These underlying libraries also have direct rows. C and C++ call sites share the same plugin.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/c/libmp3splt/README.md)

```sh
python3 parsarium.py build mp3_id3v2 c libmp3splt
python3 parsarium.py run mp3_id3v2 c libmp3splt controls/mp3_id3v2/tone-tags.mp3
```
