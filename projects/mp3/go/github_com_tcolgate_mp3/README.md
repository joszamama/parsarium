# github.com/tcolgate/mp3 — MP3 / Go

Pinned release: `v0.0.0-20170426193717-e79c5a46d300`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/go/github-com-tcolgate-mp3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 go github_com_tcolgate_mp3
python3 parsarium.py run mp3 go github_com_tcolgate_mp3 controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 go github_com_tcolgate_mp3 CORPUS_DIR runs/mp3-github_com_tcolgate_mp3-replay
python3 parsarium.py afl build mp3 go github_com_tcolgate_mp3
python3 parsarium.py afl prepare mp3 go github_com_tcolgate_mp3 runs/mp3-github_com_tcolgate_mp3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Frame parser only; does not decode PCM. Two untagged CBR controls do not establish VBR or full MPEG audio support.
