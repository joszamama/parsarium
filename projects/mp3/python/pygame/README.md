# pygame — MP3 / Python

Pinned release: `2.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/python/pygame/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 python pygame
python3 parsarium.py run mp3 python pygame controls/mp3/id3v2-tagged-tone.mp3
python3 parsarium.py replay mp3 python pygame CORPUS_DIR runs/mp3-pygame-replay
python3 parsarium.py afl build mp3 python pygame
python3 parsarium.py afl prepare mp3 python pygame runs/mp3-pygame-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Feedback scope:** AFL++ observes edges in the pinned `libmpg123-fad61782.so.0.47.0` shared library. This target does not claim source-line coverage. The verification receipt records the module hash and differential valid-control check.
