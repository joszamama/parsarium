# github.com/dmulholl/mp3lib — MP3 / Go

- **Pinned release:** `v1.0.0`
- **License:** Unlicense
- **Parsed scope:** MPEG Layer III frame headers and frame boundaries from untagged local bytes; no PCM decoding
- **Underlying family:** dmulholl/mp3lib frame parser
- **Local input API:** `NextFrame(io.Reader) *MP3Frame; MP3Frame header and frame fields`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/dmulholl/mp3lib@v1.0.0>)
- **Catalog evidence:** [parser record](../../../../data/go/mp3/parsers.json) · [control verification](../../../../data/go/mp3/verification.json) · [within-ecosystem ranking](../../../../data/go/mp3/ranking.md)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)

## Observed control result

```json
{
  "sample_rate": 44100,
  "channels": 1,
  "frames": 11,
  "frame_bytes": 2298,
  "samples_per_frame": 1152,
  "bitrate": 64000
}
```

Independent Go MP3 frame parser; can also skip ID3 tags, but the plain MP3 controls have none. Separate from tcolgate/mp3 and hajime/go-mp3.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/go/github_com_dmulholl_mp3lib/README.md)

```sh
python3 parsarium.py build mp3 go github_com_dmulholl_mp3lib
python3 parsarium.py run mp3 go github_com_dmulholl_mp3lib controls/mp3/tone-44k-mono.mp3
```

**Coverage limit:** Frame parser only; does not decode PCM. Two untagged CBR controls do not establish VBR or complete MPEG audio support.
