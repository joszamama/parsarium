# github.com/robxyy/govips/pkg/vips — ASCII PNM / Go

Pinned release: `v0.0.0-20180604122901-95ac1cf58567`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/go/github-com-robxyy-govips-pkg-vips/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm go github_com_robxyy_govips_pkg_vips
python3 parsarium.py run ascii_pnm go github_com_robxyy_govips_pkg_vips controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm go github_com_robxyy_govips_pkg_vips CORPUS_DIR runs/ascii_pnm-github_com_robxyy_govips_pkg_vips-replay
python3 parsarium.py afl build ascii_pnm go github_com_robxyy_govips_pkg_vips
python3 parsarium.py afl prepare ascii_pnm go github_com_robxyy_govips_pkg_vips runs/ascii_pnm-github_com_robxyy_govips_pkg_vips-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
