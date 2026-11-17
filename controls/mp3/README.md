# Plain MP3 controls

These are valid, untagged MPEG Layer III streams. The Rust and Go pilots use
different pinned files with overlapping descriptive names, so their control
paths and hashes remain distinct.

| Control | Bytes | SHA-256 | Use |
| --- | ---: | --- | --- |
| `tone-44k-mono.mp3` | 2,298 | `9bcbe84e7a36645c09464e671b81af90766e569d07f1b4e214b8cf87b46bf328` | Rust, C and PHP pilot primary |
| `tone-22k-stereo.mp3` | 1,254 | `871bfdb49897b4e2e1994987862aca928f4f6438f731831e3c7662579fb8c000` | Rust pilot variant; C and PHP pilot AFL++ differential |
| `go-tone-44k-mono.mp3` | 2,298 | `494492685c8ac5bfdbcbefa217c18a0fd4d2a44e21831e15a3fe0b0861d96c36` | Go pilot primary, MPEG-1 44.1 kHz mono |
| `go-tone-22k-stereo.mp3` | 1,254 | `e14721b65abfed142af10f51b43f29993a22003091eaa29086d2e36d7157761a` | Go pilot variant, MPEG-2 22.05 kHz stereo |

The Go pair was generated once with SoX and LAME 4.0, using the `-t` option to
omit Xing/LAME info frames; the exact bytes are committed. The controls test
different MPEG versions, sample rates, channel modes, and bitrates. See the
[Go pilot notes](../../projects/mp3/go/github_com_hajimehoshi_go_mp3/PROJECT_NOTES.md)
and [Rust pilot record](../../data/rust/mp3/cell.json) for parser scope.
