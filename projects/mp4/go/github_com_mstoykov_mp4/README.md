# github.com/MStoykov/mp4 — MP4 / Go

Pinned release: `v0.1.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/go/github-com-mstoykov-mp4/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 go github_com_mstoykov_mp4
python3 parsarium.py run mp4 go github_com_mstoykov_mp4 controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 go github_com_mstoykov_mp4 CORPUS_DIR runs/mp4-github_com_mstoykov_mp4-replay
python3 parsarium.py afl build mp4 go github_com_mstoykov_mp4
python3 parsarium.py afl prepare mp4 go github_com_mstoykov_mp4 runs/mp4-github_com_mstoykov_mp4-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
