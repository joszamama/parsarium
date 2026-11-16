# bento4 — MP4 / C

Pinned release: `1.6.0-641`. [Manifest](manifest.json) · [Docker receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/mp4/c/bento4/verification.json)

[API, control result, and parser family](../../../../catalog/mp4/c/bento4/README.md)

The valid MP4 control passed Docker replay and one-case fuzzer smoke, reporting the `isom` brand, two tracks and 1,000 ms duration. It covered 47 C binding lines and 1,670 underlying AP4 core lines. The AFL++ overlay observed 639 feedback edges on the same control.

The fuzzer uses AddressSanitizer. UBSan's nonnull check reports Bento4's zero-byte `memcpy` with a null pointer on this valid control, so UBSan is omitted from this harness build; the pinned Bento4 source is unchanged.

## Run from the repository root

```sh
python3 parsarium.py build mp4 c bento4
python3 parsarium.py run mp4 c bento4 controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 c bento4 CORPUS_DIR runs/mp4-bento4-replay
python3 parsarium.py afl build mp4 c bento4
python3 parsarium.py afl prepare mp4 c bento4 runs/mp4-bento4-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
