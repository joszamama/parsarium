# github.com/chenzhekl/goply — ASCII PLY / Go

Pinned release: `v0.0.0-20190930133256-258c2381defd`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/go/github-com-chenzhekl-goply/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply go github_com_chenzhekl_goply
python3 parsarium.py run ascii_ply go github_com_chenzhekl_goply controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply go github_com_chenzhekl_goply CORPUS_DIR runs/ascii_ply-github_com_chenzhekl_goply-replay
python3 parsarium.py afl build ascii_ply go github_com_chenzhekl_goply
python3 parsarium.py afl prepare ascii_ply go github_com_chenzhekl_goply runs/ascii_ply-github_com_chenzhekl_goply-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
