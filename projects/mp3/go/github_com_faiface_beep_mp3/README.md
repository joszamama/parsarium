# github.com/faiface/beep/mp3 — MP3 / Go

Pinned release: `v1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/go/github-com-faiface-beep-mp3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 go github_com_faiface_beep_mp3
python3 parsarium.py run mp3 go github_com_faiface_beep_mp3 controls/mp3/go-tone-44k-mono.mp3
python3 parsarium.py replay mp3 go github_com_faiface_beep_mp3 CORPUS_DIR runs/mp3-github_com_faiface_beep_mp3-replay
python3 parsarium.py afl build mp3 go github_com_faiface_beep_mp3
python3 parsarium.py afl prepare mp3 go github_com_faiface_beep_mp3 runs/mp3-github_com_faiface_beep_mp3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Untagged MPEG Layer III only, decoded by the wrapped go-mp3 v0.3.0 family; two valid controls do not establish complete decoder support.
