# github.com/gen2brain/pngn — PNG / Go

Pinned release: `v0.1.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/go/github-com-gen2brain-pngn/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png go github_com_gen2brain_pngn
python3 parsarium.py run png go github_com_gen2brain_pngn controls/png/red-green.png
python3 parsarium.py replay png go github_com_gen2brain_pngn CORPUS_DIR runs/png-github_com_gen2brain_pngn-replay
python3 parsarium.py afl build png go github_com_gen2brain_pngn
python3 parsarium.py afl prepare png go github_com_gen2brain_pngn runs/png-github_com_gen2brain_pngn-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
