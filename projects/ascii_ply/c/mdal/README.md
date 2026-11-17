# mdal — ASCII PLY / C

Pinned release: `1.3.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/c/mdal/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply c mdal
python3 parsarium.py run ascii_ply c mdal controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply c mdal CORPUS_DIR runs/ascii_ply-mdal-replay
python3 parsarium.py afl build ascii_ply c mdal
python3 parsarium.py afl prepare ascii_ply c mdal runs/ascii_ply-mdal-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Sanitizer exception:** The pinned libplyxx textio.h reads an unaligned uint64_t on the valid control. The AFL++ build disables Clang's alignment sanitizer only; AddressSanitizer and the other undefined-behavior checks remain enabled.
