# github.com/tosone/minimp3 — MP3 / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v1.1.0`
- **License:** MIT (Go binding); CC0-1.0 (vendored minimp3.h)
- **Parser family:** lieff/minimp3 C decoder via tosone Go cgo binding
- **Local input API:** `DecodeFull([]byte) (*Decoder, []byte, error); Decoder.SampleRate and Channels`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/tosone/minimp3@v1.1.0>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/go/mp3/parsers.json) · [control result](../../../../projects/mp3/go/github_com_tosone_minimp3/verification.json)

## Observed control result

```json
{
  "sample_rate": 44100,
  "channels": 1,
  "decoded_bytes": 25344,
  "pcm_sha256": "0641e37cb18148b29cfc23ffc8c479115a4e042a0952a91570e92888aec0a33e"
}
```

## Run this target

```sh
python3 parsarium.py build mp3 go github_com_tosone_minimp3
python3 parsarium.py run mp3 go github_com_tosone_minimp3 controls/mp3/tone-44k-mono.mp3
```
