# github.com/disintegration/imaging — PNG / Go

Pinned release: `v1.6.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/go/github-com-disintegration-imaging/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png go imaging
python3 parsarium.py run png go imaging controls/png/red-green.png
python3 parsarium.py replay png go imaging CORPUS_DIR runs/png-imaging-replay
python3 parsarium.py afl build png go imaging
python3 parsarium.py afl prepare png go imaging runs/png-imaging-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
