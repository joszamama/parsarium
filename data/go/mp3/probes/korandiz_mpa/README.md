# korandiz/mpa: excluded two-control lead

`github.com/korandiz/mpa` is a real, independent MPEG-1 Audio decoder. Its [documented `Decoder.Input io.Reader` and `DecodeFrame` API](https://pkg.go.dev/github.com/korandiz/mpa@v1.0.0#Decoder) accepts local bytes. The pinned release is `v1.0.0`, module ZIP SHA-256 `8b348db03f906aaf1bcd83d29ff702ec4eb605bb9f1a682753bac7eee00b3e5b`, Go module sum `h1:AGnEoijMfafJmf0mh08pF8z4O/Do6XdlDIVvWKLXkEw=`, and GPL-3.0 license in `LICENSE.txt`. The [saved pkg.go.dev snapshot](../../registry-snapshot.json) and [package page](https://pkg.go.dev/github.com/korandiz/mpa) report **9 Imported by** packages; this is a Go-only adoption metric, not MP3-specific use.

From this directory, run the two valid, untagged controls through the pinned API:

```sh
go run -mod=readonly . ../../../../../controls/mp3/tone-44k-mono.mp3 ../../../../../controls/mp3/tone-22k-stereo.mp3
```

The [receipt](result.json) records the observed JSON, hashes, Go version, and the independent oracle from `controls/mp3/check_controls.py`. The MPEG-1 control decodes exactly 11 frames, 44.1 kHz mono, and 12,672 samples. The MPEG-2 control should contain 12 frames, 22.05 kHz stereo, and 6,912 samples; this decoder returns `unexpected EOF` after zero frames. The package [documents MPEG-1-only scope](https://github.com/korandiz/mpa/blob/v1.0.0/doc.go#L21), and its [header validator rejects MPEG-2's `id == 0`](https://github.com/korandiz/mpa/blob/v1.0.0/decoder.go#L374).

This path is excluded from the selected plain-MP3 cell because it fails the fixed second valid control. No Docker harness, source-coverage, or AFL++ claim is made for this excluded path. The result does not imply that it fails its documented MPEG-1 scope.
