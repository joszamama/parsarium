# github.com/bu/govips/pkg/vips — ASCII PNM / Go

Pinned release: `v0.0.0-20191224162542-9c70e55b5850`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/go/github-com-bu-govips-pkg-vips/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm go github_com_bu_govips_pkg_vips
python3 parsarium.py run ascii_pnm go github_com_bu_govips_pkg_vips controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm go github_com_bu_govips_pkg_vips CORPUS_DIR runs/ascii_pnm-github_com_bu_govips_pkg_vips-replay
python3 parsarium.py afl build ascii_pnm go github_com_bu_govips_pkg_vips
python3 parsarium.py afl prepare ascii_pnm go github_com_bu_govips_pkg_vips runs/ascii_pnm-github_com_bu_govips_pkg_vips-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
