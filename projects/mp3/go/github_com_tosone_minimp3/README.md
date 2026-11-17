# github.com/tosone/minimp3 — MP3 / Go

Pinned release: `v1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/go/github-com-tosone-minimp3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 go github_com_tosone_minimp3
python3 parsarium.py run mp3 go github_com_tosone_minimp3 controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 go github_com_tosone_minimp3 CORPUS_DIR runs/mp3-github_com_tosone_minimp3-replay
python3 parsarium.py afl build mp3 go github_com_tosone_minimp3
python3 parsarium.py afl prepare mp3 go github_com_tosone_minimp3 runs/mp3-github_com_tosone_minimp3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Untagged MPEG Layer III controls only; decoder PCM differs from other implementations; no VBR, tags, Layer I/II or malformed input tested.
