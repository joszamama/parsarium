# github.com/shogo82148/go-imaging/png — PNG / Go

Pinned release: `v0.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/go/github-com-shogo82148-go-imaging-png/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png go github_com_shogo82148_go_imaging_png
python3 parsarium.py run png go github_com_shogo82148_go_imaging_png controls/png/red-green.png
python3 parsarium.py replay png go github_com_shogo82148_go_imaging_png CORPUS_DIR runs/png-github_com_shogo82148_go_imaging_png-replay
python3 parsarium.py afl build png go github_com_shogo82148_go_imaging_png
python3 parsarium.py afl prepare png go github_com_shogo82148_go_imaging_png runs/png-github_com_shogo82148_go_imaging_png-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
