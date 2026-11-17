# github.com/hajimehoshi/ebiten/v2/audio/mp3 — MP3 / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v2.10.6`
- **License:** Apache-2.0
- **Parser family:** hajime/go-mp3 lineage via Ebitengine
- **Local input API:** `DecodeWithoutResampling(io.Reader) (*Stream, error); (*Stream).Read, Length, SampleRate`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/hajimehoshi/ebiten/v2/audio/mp3@v2.10.6>)
- **Valid control:** [`controls/mp3/go-tone-44k-mono.mp3`](../../../../controls/mp3/go-tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/go/mp3/parsers.json) · [control result](../../../../projects/mp3/go/github_com_hajimehoshi_ebiten_v2_audio_mp3/verification.json)

## Observed control result

```json
{
  "sample_rate": 44100,
  "length_bytes": 50688,
  "decoded_bytes": 50688,
  "pcm_sha256": "18a327dc0181f97f5702af2a35900734e04a0f0bee3091e77580dfe5b8397304"
}
```

## Run this target

```sh
python3 parsarium.py build mp3 go github_com_hajimehoshi_ebiten_v2_audio_mp3
python3 parsarium.py run mp3 go github_com_hajimehoshi_ebiten_v2_audio_mp3 controls/mp3/go-tone-44k-mono.mp3
```
