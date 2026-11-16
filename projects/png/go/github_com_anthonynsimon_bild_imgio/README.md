# github.com/anthonynsimon/bild/imgio — PNG / Go

Pinned release: `v0.17.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/go/github-com-anthonynsimon-bild-imgio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png go github_com_anthonynsimon_bild_imgio
python3 parsarium.py run png go github_com_anthonynsimon_bild_imgio controls/png/red-green.png
python3 parsarium.py replay png go github_com_anthonynsimon_bild_imgio CORPUS_DIR runs/png-github_com_anthonynsimon_bild_imgio-replay
python3 parsarium.py afl build png go github_com_anthonynsimon_bild_imgio
python3 parsarium.py afl prepare png go github_com_anthonynsimon_bild_imgio runs/png-github_com_anthonynsimon_bild_imgio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
