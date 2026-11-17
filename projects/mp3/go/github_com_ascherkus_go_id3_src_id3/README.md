# github.com/ascherkus/go-id3/src/id3 — MP3 / Go

Pinned release: `v0.0.0-20120522061058-b139b6a612de`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/go/github-com-ascherkus-go-id3-src-id3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 go github_com_ascherkus_go_id3_src_id3
python3 parsarium.py run mp3 go github_com_ascherkus_go_id3_src_id3 controls/mp3/id3v2-tagged-tone-44k.mp3
python3 parsarium.py replay mp3 go github_com_ascherkus_go_id3_src_id3 CORPUS_DIR runs/mp3-github_com_ascherkus_go_id3_src_id3-replay
python3 parsarium.py afl build mp3 go github_com_ascherkus_go_id3_src_id3
python3 parsarium.py afl prepare mp3 go github_com_ascherkus_go_id3_src_id3 runs/mp3-github_com_ascherkus_go_id3_src_id3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
