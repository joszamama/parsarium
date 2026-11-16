# msh_ply — ASCII PLY / C

Pinned release: `1.02`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/c/msh-ply/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply c msh_ply
python3 parsarium.py run ascii_ply c msh_ply controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply c msh_ply CORPUS_DIR runs/ascii_ply-msh_ply-replay
python3 parsarium.py afl build ascii_ply c msh_ply
python3 parsarium.py afl prepare ascii_ply c msh_ply runs/ascii_ply-msh_ply-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** The base libFuzzer valid control returns expected fields while UBSan reports misaligned int32_t accesses in upstream msh_ply.h lines 1436 and 969. The AFL++ valid control trapped with alignment checks enabled, so its build adds -fno-sanitize=alignment while retaining AddressSanitizer and other UBSan checks.
