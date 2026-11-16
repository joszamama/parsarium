# github.com/magical/png — PNG / Go

Pinned release: `v0.0.0-20131112000825-bf2aaca8f4d6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/go/github-com-magical-png/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png go github_com_magical_png
python3 parsarium.py run png go github_com_magical_png controls/png/red-green.png
python3 parsarium.py replay png go github_com_magical_png CORPUS_DIR runs/png-github_com_magical_png-replay
python3 parsarium.py afl build png go github_com_magical_png
python3 parsarium.py afl prepare png go github_com_magical_png runs/png-github_com_magical_png-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
