# github.com/bogem/id3v2/v2 — MP3 / Go

Pinned release: `v2.1.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/go/github-com-bogem-id3v2-v2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 go github_com_bogem_id3v2_v2
python3 parsarium.py run mp3 go github_com_bogem_id3v2_v2 controls/mp3/id3v2-tagged-tone-44k.mp3
python3 parsarium.py replay mp3 go github_com_bogem_id3v2_v2 CORPUS_DIR runs/mp3-github_com_bogem_id3v2_v2-replay
python3 parsarium.py afl build mp3 go github_com_bogem_id3v2_v2
python3 parsarium.py afl prepare mp3 go github_com_bogem_id3v2_v2 runs/mp3-github_com_bogem_id3v2_v2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
