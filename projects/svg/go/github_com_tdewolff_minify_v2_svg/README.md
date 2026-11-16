# github.com/tdewolff/minify/v2/svg — SVG / Go

Pinned release: `v2.24.25`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/go/github-com-tdewolff-minify-v2-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg go github_com_tdewolff_minify_v2_svg
python3 parsarium.py run svg go github_com_tdewolff_minify_v2_svg controls/svg/red-green.svg
python3 parsarium.py replay svg go github_com_tdewolff_minify_v2_svg CORPUS_DIR runs/svg-github_com_tdewolff_minify_v2_svg-replay
python3 parsarium.py afl build svg go github_com_tdewolff_minify_v2_svg
python3 parsarium.py afl prepare svg go github_com_tdewolff_minify_v2_svg runs/svg-github_com_tdewolff_minify_v2_svg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
