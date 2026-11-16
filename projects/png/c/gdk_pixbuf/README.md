# gdk-pixbuf — PNG / C

Pinned release: `2.44.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/c/gdk-pixbuf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png c gdk_pixbuf
python3 parsarium.py run png c gdk_pixbuf controls/png/red-green.png
python3 parsarium.py replay png c gdk_pixbuf CORPUS_DIR runs/png-gdk_pixbuf-replay
python3 parsarium.py afl build png c gdk_pixbuf
python3 parsarium.py afl prepare png c gdk_pixbuf runs/png-gdk_pixbuf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
