# mattetti/audio/mp3: excluded by the feedback gate

`github.com/mattetti/audio/mp3` reads MPEG audio frames from an `io.Reader`. Its [documented `New(io.Reader)` and `Decoder.Next(*Frame)`](https://pkg.go.dev/github.com/mattetti/audio/mp3@v0.0.0-20240411020228-c5379f9b5b61) read each header and frame body, and `FrameHeader` reports version, layer, bitrate, sample rate, channel mode, samples and size. The package says it uses some code from `tcolgate/mp3`, but its decoder and header code are separate. The pinned release is `v0.0.0-20240411020228-c5379f9b5b61`, module ZIP SHA-256 `ad0c168c6db73a17d8891adefce9340142015318491536853713890f0056dafb`, Go module sum `h1:db1I7R9KTRARpVXhyd4+cGecxutdJbpx11Gun98GP7U=`, MIT. The [saved pkg.go.dev snapshot](../../registry-snapshot.json) reports **2 Imported by** packages. The repository README points to `go-audio` for its maintained code.

The [adapter](adapter.go) loops over `Next` until EOF and requires no skipped bytes and frame sizes that add up to the file length. From the repository root:

```sh
docker run --rm --platform linux/arm64 -v "$PWD/data/go/mp3/probes/mattetti_audio_mp3:/probe:ro" \
  -v "$PWD/controls/mp3:/controls:ro" \
  golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 sh /probe/run.sh
```

Both untagged Go controls match `controls/mp3/check_controls.py`: 11 frames, 2,298 bytes, 44.1 kHz mono, 1,152 samples per frame, 64 kbit/s; and 12 frames, 1,254 bytes, 22.05 kHz stereo, 576 samples per frame, 32 kbit/s. Each control was parsed twice. The covered `mattetti/audio/mp3` Go cover blocks repeat exactly, 38 blocks per control, but both controls cover the **same 38 blocks**. The Rust plain-MP3 pair gives the same result.

The Go AFL++ bridge maps exactly these blocks to tuples, so the path cannot show input-dependent parser feedback on the valid controls. It is excluded from the selected cell under the runnability gate. No Docker harness or AFL++ overlay is claimed. This does not deny that the package parses the controls. [result.json](result.json) records the observations.
