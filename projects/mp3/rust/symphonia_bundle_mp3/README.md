# symphonia-bundle-mp3 — MP3 / Rust

Pinned release: `0.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/mp3/rust/symphonia_bundle_mp3/verification.json)

[API, control result, and parser family](../../../../catalog/mp3/rust/symphonia-bundle-mp3/README.md)

The harness (`src/lib.rs`) demuxes every MPEG audio frame from an in-memory byte stream and decodes it. It reports the frame count, the frame bytes, and the decoded samples. The input has no ID3 tag, so tag parsing cannot satisfy the control.

## Run from the repository root

```sh
python3 parsarium.py build mp3 rust symphonia_bundle_mp3
python3 parsarium.py run mp3 rust symphonia_bundle_mp3 controls/mp3/tone-44k-mono.mp3
python3 parsarium.py afl build mp3 rust symphonia_bundle_mp3
python3 parsarium.py afl prepare mp3 rust symphonia_bundle_mp3 runs/mp3-symphonia_bundle_mp3-afl
python3 parsarium.py afl run runs/mp3-symphonia_bundle_mp3-afl --check
```

`afl build` builds the afl.rs overlay. It then runs `afl-showmap` three times on each of the two fixed valid controls and records the edge counts and their stability. The AFL++ commands prepare and check a seeded run; they do not start a campaign.
