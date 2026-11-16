# libimago — ASCII PNM / C

Pinned release: `2.4.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/c/libimago/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm c libimago
python3 parsarium.py run ascii_pnm c libimago controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm c libimago CORPUS_DIR runs/ascii_pnm-libimago-replay
python3 parsarium.py afl build ascii_pnm c libimago
python3 parsarium.py afl prepare ascii_pnm c libimago runs/ascii_pnm-libimago-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
