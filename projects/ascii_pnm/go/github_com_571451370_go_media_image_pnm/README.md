# github.com/571451370/go-media/image/pnm — ASCII PNM / Go

Pinned release: `v0.0.0-20190312080447-697b98554cbd`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/go/github-com-571451370-go-media-image-pnm/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm go github_com_571451370_go_media_image_pnm
python3 parsarium.py run ascii_pnm go github_com_571451370_go_media_image_pnm controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm go github_com_571451370_go_media_image_pnm CORPUS_DIR runs/ascii_pnm-github_com_571451370_go_media_image_pnm-replay
python3 parsarium.py afl build ascii_pnm go github_com_571451370_go_media_image_pnm
python3 parsarium.py afl prepare ascii_pnm go github_com_571451370_go_media_image_pnm runs/ascii_pnm-github_com_571451370_go_media_image_pnm-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
