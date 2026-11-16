# bento4 — MP4 / C

Pinned release: `1.6.0-641`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/c/bento4/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 c bento4
python3 parsarium.py run mp4 c bento4 controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 c bento4 CORPUS_DIR runs/mp4-bento4-replay
python3 parsarium.py afl build mp4 c bento4
python3 parsarium.py afl prepare mp4 c bento4 runs/mp4-bento4-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Sanitizer exception:** The pinned Bento4 AP4 core calls memcpy with a null pointer and zero length on the valid MP4 control. UBSan's nonnull check reports this upstream call, so this harness uses AddressSanitizer without UBSan; the pinned source is unchanged.
