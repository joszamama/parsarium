# github.com/kovidgoyal/imaging — ASCII PNM / Go

Pinned release: `v1.9.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/go/github-com-kovidgoyal-imaging/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm go github_com_kovidgoyal_imaging
python3 parsarium.py run ascii_pnm go github_com_kovidgoyal_imaging controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm go github_com_kovidgoyal_imaging CORPUS_DIR runs/ascii_pnm-github_com_kovidgoyal_imaging-replay
python3 parsarium.py afl build ascii_pnm go github_com_kovidgoyal_imaging
python3 parsarium.py afl prepare ascii_pnm go github_com_kovidgoyal_imaging runs/ascii_pnm-github_com_kovidgoyal_imaging-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
