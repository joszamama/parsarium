# github.com/go-forks/go-pkg-xmlx — XML / Go

Pinned release: `v0.0.0-20151201012946-76f54ee73233`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/go/github-com-go-forks-go-pkg-xmlx/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml go github_com_go_forks_go_pkg_xmlx
python3 parsarium.py run xml go github_com_go_forks_go_pkg_xmlx controls/xml/catalog-ns.xml
python3 parsarium.py replay xml go github_com_go_forks_go_pkg_xmlx CORPUS_DIR runs/xml-github_com_go_forks_go_pkg_xmlx-replay
python3 parsarium.py afl build xml go github_com_go_forks_go_pkg_xmlx
python3 parsarium.py afl prepare xml go github_com_go_forks_go_pkg_xmlx runs/xml-github_com_go_forks_go_pkg_xmlx-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
