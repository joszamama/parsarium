# github.com/dsoprea/go-png-image-structure/v2 — PNG / Go

Pinned release: `v2.0.0-20210512210324-29b889a6093d`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/go/github-com-dsoprea-go-png-image-structure-v2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png go github_com_dsoprea_go_png_image_structure_v2
python3 parsarium.py run png go github_com_dsoprea_go_png_image_structure_v2 controls/png/red-green.png
python3 parsarium.py replay png go github_com_dsoprea_go_png_image_structure_v2 CORPUS_DIR runs/png-github_com_dsoprea_go_png_image_structure_v2-replay
python3 parsarium.py afl build png go github_com_dsoprea_go_png_image_structure_v2
python3 parsarium.py afl prepare png go github_com_dsoprea_go_png_image_structure_v2 runs/png-github_com_dsoprea_go_png_image_structure_v2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
