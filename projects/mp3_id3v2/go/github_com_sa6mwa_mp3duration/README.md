# github.com/sa6mwa/mp3duration — MP3 with ID3v2 / Go

Pinned release: `v0.0.0-20221104103912-0716b1a5de6e`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/go/github-com-sa6mwa-mp3duration/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 go github_com_sa6mwa_mp3duration
python3 parsarium.py run mp3_id3v2 go github_com_sa6mwa_mp3duration controls/mp3_id3v2/tone-tags-44k.mp3
python3 parsarium.py replay mp3_id3v2 go github_com_sa6mwa_mp3duration CORPUS_DIR runs/mp3_id3v2-github_com_sa6mwa_mp3duration-replay
python3 parsarium.py afl build mp3_id3v2 go github_com_sa6mwa_mp3duration
python3 parsarium.py afl prepare mp3_id3v2 go github_com_sa6mwa_mp3duration runs/mp3_id3v2-github_com_sa6mwa_mp3duration-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
