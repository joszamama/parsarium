# tcolgate/mp3 — plain MP3 / Go

Pinned [MIT-licensed release](https://pkg.go.dev/github.com/tcolgate/mp3@v0.0.0-20170426193717-e79c5a46d300) `v0.0.0-20170426193717-e79c5a46d300`. This package parses MPEG audio frame headers and boundaries; it does not decode PCM. Its 62 pkg.go.dev “Imported by” packages are an adoption proxy for the package, not a count of MP3 decoding users. The parser is also represented in the tagged MP3 cell. The `fgergo/mp3` fork shares its lineage.

The adapter reads a local file, passes its bytes to `mp3.NewDecoder(io.Reader)`, calls `Decoder.Decode` until EOF, and reports fields from `Frame.Header`, `Frame.Size`, and `Frame.Samples`. The two valid untagged controls match the independent header walker in [the control checker](../../../../controls/mp3/check_controls.py): 11 MPEG-1 mono 44.1 kHz frames and 12 MPEG-2 stereo 22.05 kHz frames. Only these constant-bitrate cases are established.

The [manifest](manifest.json), [project receipt](verification.json), [AFL++ receipt](../../../../fuzzing/afl-native/mp3/go/github_com_tcolgate_mp3/verification.json), and [valid-control differential](../../../../fuzzing/afl-native/mp3/go/github_com_tcolgate_mp3/differential.json) record pins and observed feedback. Coverage includes 70 package source lines, 64 in `frames.go`. The AFL++ bridge observes 44 package source features and 64 tuples on the first control; three features and three tuples differ on the second control. Two repeats per control matched exactly. The bridge instruments the Go package's parser lines, not merely the harness.

Run from the repository root:

```sh
python3 parsarium.py build mp3 go github_com_tcolgate_mp3
python3 parsarium.py run mp3 go github_com_tcolgate_mp3 controls/mp3/tone-44k-mono.mp3
python3 parsarium.py afl build mp3 go github_com_tcolgate_mp3
python3 scripts/smoke_pilot_differential.py mp3 go github_com_tcolgate_mp3
python3 parsarium.py afl prepare mp3 go github_com_tcolgate_mp3 runs/mp3-go-tcolgate-afl \
  --seed controls/mp3/tone-22k-stereo.mp3
python3 parsarium.py afl run runs/mp3-go-tcolgate-afl --check
```

`--check` validates the AFL++ command and seed layout without starting a campaign. Fandango can generate valid format seeds separately; the shared `parsarium.py fandango` commands prepare those seeds for replay or AFL++. Neither a vulnerability nor malformed-input claim follows from these controls.
