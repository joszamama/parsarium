# javasound-aac — MP4 / Java

Pinned release: `0.9.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/java/javasound-aac/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 java javasound_aac
python3 parsarium.py run mp4 java javasound_aac controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 java javasound_aac CORPUS_DIR runs/mp4-javasound_aac-replay
python3 parsarium.py afl build mp4 java javasound_aac
python3 parsarium.py afl prepare mp4 java javasound_aac runs/mp4-javasound_aac-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
