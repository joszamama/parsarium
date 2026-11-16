# github.com/git-pkgs/archives — ZIP / Go

Pinned release: `v0.11.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-git-pkgs-archives/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go github_com_git_pkgs_archives
python3 parsarium.py run zip go github_com_git_pkgs_archives controls/zip/hello.zip
python3 parsarium.py replay zip go github_com_git_pkgs_archives CORPUS_DIR runs/zip-github_com_git_pkgs_archives-replay
python3 parsarium.py afl build zip go github_com_git_pkgs_archives
python3 parsarium.py afl prepare zip go github_com_git_pkgs_archives runs/zip-github_com_git_pkgs_archives-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
