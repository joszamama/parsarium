# tosone/minimp3 — plain MP3 / Go

Pinned [Go binding release](https://pkg.go.dev/github.com/tosone/minimp3) `v1.1.0` (MIT); its vendored [`minimp3.h`](https://github.com/lieff/minimp3) decoder is CC0-1.0. The package has **34 pkg.go.dev “Imported by” packages** in the saved search snapshot. That measures imports of this package, not MP3 decoding use. This is a separate decoder family from `hajimehoshi/go-mp3` and from the Go frame parsers.

The adapter passes local bytes to the documented `DecodeFull([]byte)` API and reports sample rate, channels, decoded byte count, and a PCM SHA-256. Both small, valid, untagged constant-bitrate controls produce decoded lengths implied by the independent [MPEG frame walker](../../../../controls/mp3/check_controls.py): 11 × 1,152 mono 16-bit samples and 12 × 576 stereo 16-bit samples. The PCM hashes are pinned to the Clang-built linux/arm64 container; the same release compiled with GCC produced different PCM hashes on these controls, so hashes are not compared across toolchains.

The [manifest](manifest.json), [project receipt](verification.json), [native AFL++ receipt](../../../../fuzzing/afl-native/mp3/go/github_com_tosone_minimp3/verification.json), and [feedback validation](../../../../fuzzing/afl-native/mp3/go/github_com_tosone_minimp3/feedback-validation.json) record the exact builds and observations. Go coverpkg reports 23 binding lines. Clang/LLVM records 885 counted decoder lines in `minimp3.h`; the exported line view shows 918 positive-count lines, including macro expansion sites. They are labeled separately in the coverage output.

AFL++ compiles the vendored C decoder through the Go cgo binding. Its [47-function allowlist](afl-allowlist.txt) comes from functions whose LLVM source mapping points to `minimp3.h`; Go runtime and generated cgo glue are excluded from AFL feedback. Five repeated runs of each valid control produced identical maps: 76 and 48 native decoder tuples respectively, with 44 tuple IDs differing between controls. No campaign or malformed input was run.

Run from the repository root:

```sh
python3 parsarium.py build mp3 go github_com_tosone_minimp3
python3 parsarium.py run mp3 go github_com_tosone_minimp3 controls/mp3/tone-44k-mono.mp3
python3 parsarium.py afl build mp3 go github_com_tosone_minimp3
python3 parsarium.py afl prepare mp3 go github_com_tosone_minimp3 runs/mp3-go-minimp3-afl \
  --seed controls/mp3/tone-22k-stereo.mp3
python3 parsarium.py afl run runs/mp3-go-minimp3-afl --check
```

The prepared AFL++ command uses `/work/afl-target @@` and native decoder feedback. `--check` validates it without starting a campaign. These controls do not establish VBR, tagged MP3, Layer I/II, MPEG-2.5, or general decoding correctness.
