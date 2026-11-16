# github.com/frolovo22/tag — MP3 with ID3v2 / Go

Pinned release: `v0.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3_id3v2/go/github-com-frolovo22-tag/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 go github_com_frolovo22_tag
python3 parsarium.py run mp3_id3v2 go github_com_frolovo22_tag controls/mp3_id3v2/tone-tags-44k.mp3
python3 parsarium.py replay mp3_id3v2 go github_com_frolovo22_tag CORPUS_DIR runs/mp3_id3v2-github_com_frolovo22_tag-replay
python3 parsarium.py afl build mp3_id3v2 go github_com_frolovo22_tag
python3 parsarium.py afl prepare mp3_id3v2 go github_com_frolovo22_tag runs/mp3_id3v2-github_com_frolovo22_tag-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
