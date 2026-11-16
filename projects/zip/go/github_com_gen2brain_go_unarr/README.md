# github.com/gen2brain/go-unarr — ZIP / Go

Pinned release: `v0.2.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-gen2brain-go-unarr/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go github_com_gen2brain_go_unarr
python3 parsarium.py run zip go github_com_gen2brain_go_unarr controls/zip/hello.zip
python3 parsarium.py replay zip go github_com_gen2brain_go_unarr CORPUS_DIR runs/zip-github_com_gen2brain_go_unarr-replay
python3 parsarium.py afl build zip go github_com_gen2brain_go_unarr
python3 parsarium.py afl prepare zip go github_com_gen2brain_go_unarr runs/zip-github_com_gen2brain_go_unarr-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
