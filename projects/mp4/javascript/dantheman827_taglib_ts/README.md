# @dantheman827/taglib-ts — MP4 / JavaScript

Pinned release: `0.1.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/javascript/dantheman827-taglib-ts/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 javascript dantheman827_taglib_ts
python3 parsarium.py run mp4 javascript dantheman827_taglib_ts controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 javascript dantheman827_taglib_ts CORPUS_DIR runs/mp4-dantheman827_taglib_ts-replay
python3 parsarium.py afl build mp4 javascript dantheman827_taglib_ts
python3 parsarium.py afl prepare mp4 javascript dantheman827_taglib_ts runs/mp4-dantheman827_taglib_ts-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
