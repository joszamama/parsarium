# dmulholl/mp3lib — plain MP3 / Go

Pinned [Unlicense release](https://pkg.go.dev/github.com/dmulholl/mp3lib@v1.0.0) `v1.0.0`. The public pkg.go.dev count is **9 “Imported by” packages**, an adoption proxy for the package rather than measured MP3 use. Higher-adoption `tosone/minimp3` remains under native C instrumentation review; this entry does not claim a definitive top-three ranking.

The adapter reads a local file and repeatedly calls `mp3lib.NextFrame(io.Reader)`. `MP3Frame` provides version, layer, sample rate, channel mode, bitrate, frame length, and sample count. Its source parses frame headers and copies full frames; it does not decode PCM. The two untagged constant-bitrate controls match [the independent header walker](../../../../controls/mp3/check_controls.py) on all reported fields, including 11 MPEG-1 frames at 44.1 kHz and 12 MPEG-2 frames at 22.05 kHz. The adapter checks that parsed frame lengths consume the whole file.

The [manifest](manifest.json), [project receipt](verification.json), [AFL++ receipt](../../../../fuzzing/afl-native/mp3/go/github_com_dmulholl_mp3lib/verification.json), and [valid-control differential](../../../../fuzzing/afl-native/mp3/go/github_com_dmulholl_mp3lib/differential.json) pin the release and results. Coverage includes 58 package source lines in `mp3lib.go`. The AFL++ bridge has 47 source features and 67 tuples on the first control; 10 features and 10 tuples differ for the second valid control. Two repeats of each control matched exactly.

Run from the repository root:

```sh
python3 parsarium.py build mp3 go github_com_dmulholl_mp3lib
python3 parsarium.py run mp3 go github_com_dmulholl_mp3lib controls/mp3/tone-44k-mono.mp3
python3 parsarium.py afl build mp3 go github_com_dmulholl_mp3lib
python3 scripts/smoke_pilot_differential.py mp3 go github_com_dmulholl_mp3lib
python3 parsarium.py afl prepare mp3 go github_com_dmulholl_mp3lib runs/mp3-go-mp3lib-afl \
  --seed controls/mp3/tone-22k-stereo.mp3
python3 parsarium.py afl run runs/mp3-go-mp3lib-afl --check
```

`--check` validates the seeded AFL++ command without starting a campaign. These two valid controls do not establish support for VBR, ID3 tags, Layer I/II, or every MPEG version.
