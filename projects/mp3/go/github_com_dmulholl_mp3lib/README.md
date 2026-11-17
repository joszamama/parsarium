# github.com/dmulholl/mp3lib — MP3 / Go

Pinned release: `v1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/go/github-com-dmulholl-mp3lib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 go github_com_dmulholl_mp3lib
python3 parsarium.py run mp3 go github_com_dmulholl_mp3lib controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 go github_com_dmulholl_mp3lib CORPUS_DIR runs/mp3-github_com_dmulholl_mp3lib-replay
python3 parsarium.py afl build mp3 go github_com_dmulholl_mp3lib
python3 parsarium.py afl prepare mp3 go github_com_dmulholl_mp3lib runs/mp3-github_com_dmulholl_mp3lib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Frame parser only; does not decode PCM. Two untagged CBR controls do not establish VBR or complete MPEG audio support.
