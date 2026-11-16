# github.com/pydpll/dedalo/obj — ASCII PLY / Go

Pinned release: `v0.0.0-20260811120505-e095fa690fcf`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/go/github-com-pydpll-dedalo-obj/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply go github_com_pydpll_dedalo_obj
python3 parsarium.py run ascii_ply go github_com_pydpll_dedalo_obj controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply go github_com_pydpll_dedalo_obj CORPUS_DIR runs/ascii_ply-github_com_pydpll_dedalo_obj-replay
python3 parsarium.py afl build ascii_ply go github_com_pydpll_dedalo_obj
python3 parsarium.py afl prepare ascii_ply go github_com_pydpll_dedalo_obj runs/ascii_ply-github_com_pydpll_dedalo_obj-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
