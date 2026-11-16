# fmonts/ffmpeg-bundle — MP4 / PHP

Pinned release: `0.8.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/php/fmonts-ffmpeg-bundle/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 php fmonts_ffmpeg_bundle
python3 parsarium.py run mp4 php fmonts_ffmpeg_bundle controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 php fmonts_ffmpeg_bundle CORPUS_DIR runs/mp4-fmonts_ffmpeg_bundle-replay
python3 parsarium.py afl build mp4 php fmonts_ffmpeg_bundle
python3 parsarium.py afl prepare mp4 php fmonts_ffmpeg_bundle runs/mp4-fmonts_ffmpeg_bundle-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
