# github.com/guregu/tag — MP4 / Go

Pinned release: `v0.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/go/github-com-guregu-tag/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 go github_com_guregu_tag
python3 parsarium.py run mp4 go github_com_guregu_tag controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 go github_com_guregu_tag CORPUS_DIR runs/mp4-github_com_guregu_tag-replay
python3 parsarium.py afl build mp4 go github_com_guregu_tag
python3 parsarium.py afl prepare mp4 go github_com_guregu_tag runs/mp4-github_com_guregu_tag-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
