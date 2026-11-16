# node-video-lib — MP4 / JavaScript

Pinned release: `2.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/javascript/node-video-lib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 javascript node_video_lib
python3 parsarium.py run mp4 javascript node_video_lib controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 javascript node_video_lib CORPUS_DIR runs/mp4-node_video_lib-replay
python3 parsarium.py afl build mp4 javascript node_video_lib
python3 parsarium.py afl prepare mp4 javascript node_video_lib runs/mp4-node_video_lib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
