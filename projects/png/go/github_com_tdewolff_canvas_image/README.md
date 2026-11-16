# github.com/tdewolff/canvas/image — PNG / Go

Pinned release: `v0.0.0-20260923214215-09804640d00c`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/go/github-com-tdewolff-canvas-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png go github_com_tdewolff_canvas_image
python3 parsarium.py run png go github_com_tdewolff_canvas_image controls/png/red-green.png
python3 parsarium.py replay png go github_com_tdewolff_canvas_image CORPUS_DIR runs/png-github_com_tdewolff_canvas_image-replay
python3 parsarium.py afl build png go github_com_tdewolff_canvas_image
python3 parsarium.py afl prepare png go github_com_tdewolff_canvas_image runs/png-github_com_tdewolff_canvas_image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
