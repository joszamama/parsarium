# github.com/davidbyttow/govips/v2/vips — PNG / Go

Pinned release: `v2.20.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/go/github-com-davidbyttow-govips-v2-vips/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png go github_com_davidbyttow_govips_v2_vips
python3 parsarium.py run png go github_com_davidbyttow_govips_v2_vips controls/png/red-green.png
python3 parsarium.py replay png go github_com_davidbyttow_govips_v2_vips CORPUS_DIR runs/png-github_com_davidbyttow_govips_v2_vips-replay
python3 parsarium.py afl build png go github_com_davidbyttow_govips_v2_vips
python3 parsarium.py afl prepare png go github_com_davidbyttow_govips_v2_vips runs/png-github_com_davidbyttow_govips_v2_vips-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
