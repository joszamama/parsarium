# github.com/hajimehoshi/go-mp3 — plain MP3 / Go (pilot)

Pinned release: `v0.3.4` (Apache-2.0, module zip SHA-256 `c14676f9…f311`). [Manifest](manifest.json) · [verification receipt](verification.json) · [AFL++ bridge receipt](../../../../fuzzing/afl-native/mp3/go/github_com_hajimehoshi_go_mp3/verification.json) · [differential receipt](../../../../fuzzing/afl-native/mp3/go/github_com_hajimehoshi_go_mp3/differential.json) · [pilot registry](../../../../data/FORMAT_PILOTS.md)

This is a pilot outside the ten-format catalog. It is separate from the `mp3_id3v2` go-mp3 project in three ways:

- The input must be an untagged MP3. The adapter rejects an `ID3` prefix or a `TAG` trailer before calling the parser.
- The result comes from decoded audio: sample rate from the first frame header, `Length()` from a scan of every frame, the PCM byte count, and the SHA-256 of the decoded PCM.
- Coverage spans `github.com/hajimehoshi/go-mp3/...`, including the internal frame header, side info, main data, Huffman and IMDCT packages. The `mp3_id3v2` project covers only the root package.

## Parser API

`mp3.NewDecoder(io.Reader) (*Decoder, error)` on a `bytes.Reader` over the local file, then `io.Copy` from the decoder (its `Read`), `SampleRate()` and `Length()`. These are documented at [pkg.go.dev](https://pkg.go.dev/github.com/hajimehoshi/go-mp3@v0.3.4). Decoded output is capped at 64 MiB.

## Controls

| Control | Observed |
| --- | --- |
| [`go-tone-44k-mono.mp3`](../../../../controls/mp3/go-tone-44k-mono.mp3) (MPEG-1, 44.1 kHz mono) | `sample_rate` 44100, `length_bytes` 50688, `decoded_bytes` 50688, `pcm_sha256` `18a327dc…7304` |
| [`go-tone-22k-stereo.mp3`](../../../../controls/mp3/go-tone-22k-stereo.mp3) (MPEG-2, 22.05 kHz joint stereo) | `sample_rate` 22050, `length_bytes` 27648, `decoded_bytes` 27648, `pcm_sha256` `454a8580…a0a9` |

go-mp3 always emits 16-bit stereo PCM, so both lengths are four bytes per sample (11 MPEG-1 frames of 1,152 samples; 12 MPEG-2 frames of 576 samples). The PCM hash was observed on linux/arm64 in the pinned image. go-mp3 decodes with floating point, so another architecture may give a different hash.

## Coverage and feedback

- Primary control: 680 of 1,018 go-mp3 statements in 10 files (641 source lines), including 80 lines of `internal/frameheader/frameheader.go`.
- AFL++ bridge: 406 parser blocks and 426 AFL++ tuples on the primary control.
- Differential: each control was traced twice through the bridge, and the repeats matched exactly. The two controls differ in 112 parser blocks and 111 AFL++ tuples. The differences are mostly in `maindata`, `frameheader`, `frame` and `sideinfo`. The second control's decoded output was checked against its pinned value in the base image.

## Run from the repository root

```sh
python3 parsarium.py build mp3 go github_com_hajimehoshi_go_mp3
python3 parsarium.py run mp3 go github_com_hajimehoshi_go_mp3 controls/mp3/go-tone-44k-mono.mp3
python3 parsarium.py afl build mp3 go github_com_hajimehoshi_go_mp3
python3 scripts/smoke_pilot_differential.py mp3 go github_com_hajimehoshi_go_mp3
python3 parsarium.py afl prepare mp3 go github_com_hajimehoshi_go_mp3 runs/mp3-go-mp3-afl \
  --seed controls/mp3/go-tone-22k-stereo.mp3
python3 parsarium.py afl run runs/mp3-go-mp3-afl --check
```

`afl prepare` and `--check` pin a seeded run; they do not start a campaign. Like other Go projects, the `run` receipt records whether the harness finished and the go-mp3 coverage percentage. It does not print the decoded fields.
