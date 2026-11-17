# derat/mpeg: excluded by the feedback gate

`github.com/derat/mpeg` has its own MPEG audio header reader. Its [documented `ReadFrameInfo(*os.File, int64)`](https://pkg.go.dev/github.com/derat/mpeg@v0.0.0-20230417205750-1ba0e56ec731#ReadFrameInfo) reads the four-byte header at an offset and returns bitrate, sample rate, samples per frame, channel mode, CRC and padding; `FrameInfo.Size()` gives the frame length. The pinned release is `v0.0.0-20230417205750-1ba0e56ec731`, module ZIP SHA-256 `c297a41b19f8f195be9962ba1c037337c0318089cafda880a6865d4aa01c6273`, Go module sum `h1:Bpf0HGJMtarpt5RFdSkoKOs/1MuYl1gj0psLNDn+0NE=`, BSD-3-Clause. The [saved pkg.go.dev snapshot](../../registry-snapshot.json) reports **3 Imported by** packages. The repository README says the module moved to `codeberg.org/derat/mpeg` (also 3 Imported by in the snapshot); that release keeps the same `ReadFrameInfo` and `Size` code.

The [adapter](adapter.go) rejects ID3 tags, then calls `ReadFrameInfo` at offset 0 and advances by `Size()` until the file ends on a frame boundary. From the repository root, run it in the pinned Go image:

```sh
docker run --rm --platform linux/arm64 -v "$PWD/data/go/mp3/probes/derat_mpeg:/probe:ro" \
  -v "$PWD/controls/mp3:/controls:ro" \
  golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 sh /probe/run.sh
```

Both untagged Go controls match `controls/mp3/check_controls.py`: 11 frames, 2,298 bytes, 44.1 kHz mono, 1,152 samples per frame, 64 kbit/s; and 12 frames, 1,254 bytes, 22.05 kHz stereo, 576 samples per frame, 32 kbit/s. Each control was parsed twice. The covered `derat/mpeg` Go cover blocks repeat exactly, 14 blocks per control, but the two controls cover the **same 14 blocks**. The header fields come from table lookups, so MPEG-1 and MPEG-2 take the same branches. The Rust plain-MP3 pair (`tone-44k-mono.mp3`, `tone-22k-stereo.mp3`) also gives 14 identical blocks.

The Go AFL++ bridge maps exactly these covered blocks to tuples, so the path cannot show input-dependent parser feedback on the valid controls. It is excluded from the selected cell under the runnability gate. No Docker harness or AFL++ overlay is claimed. This does not deny that the package parses the controls. [result.json](result.json) records the observations.
