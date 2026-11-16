# gdk-pixbuf — ASCII PNM / C

Pinned release: `2.44.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/c/gdk-pixbuf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm c gdk_pixbuf
python3 parsarium.py run ascii_pnm c gdk_pixbuf controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm c gdk_pixbuf CORPUS_DIR runs/ascii_pnm-gdk_pixbuf-replay
python3 parsarium.py afl build ascii_pnm c gdk_pixbuf
python3 parsarium.py afl prepare ascii_pnm c gdk_pixbuf runs/ascii_pnm-gdk_pixbuf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
