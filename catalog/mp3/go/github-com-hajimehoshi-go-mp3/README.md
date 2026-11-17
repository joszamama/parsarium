# github.com/hajimehoshi/go-mp3 — MP3 / Go

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v0.3.4`
- **License:** Apache-2.0
- **Parser family:** hajime/go-mp3 lineage
- **Local input API:** `NewDecoder(io.Reader) (*Decoder, error); Read([]byte); SampleRate(); Length()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/hajimehoshi/go-mp3@v0.3.4>)
- **Valid control:** [`controls/mp3/go-tone-44k-mono.mp3`](../../../../controls/mp3/go-tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/go/mp3/parsers.json) · [control result](../../../../projects/mp3/go/github_com_hajimehoshi_go_mp3/verification.json)

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
python3 parsarium.py build mp3 go github_com_hajimehoshi_go_mp3
python3 parsarium.py run mp3 go github_com_hajimehoshi_go_mp3 controls/mp3/go-tone-44k-mono.mp3
```
