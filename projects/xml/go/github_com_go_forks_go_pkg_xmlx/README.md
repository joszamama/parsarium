# github.com/go-forks/go-pkg-xmlx — XML / Go

Pinned release: `v0.0.0-20151201012946-76f54ee73233`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/go/github-com-go-forks-go-pkg-xmlx/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml go github_com_go_forks_go_pkg_xmlx
python3 parsarium.py run xml go github_com_go_forks_go_pkg_xmlx controls/xml/catalog-ns.xml
python3 parsarium.py replay xml go github_com_go_forks_go_pkg_xmlx CORPUS_DIR runs/xml-github_com_go_forks_go_pkg_xmlx-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build xml go github_com_go_forks_go_pkg_xmlx
python3 parsarium.py afl prepare xml go github_com_go_forks_go_pkg_xmlx runs/xml-github_com_go_forks_go_pkg_xmlx-afl --fandango 100
python3 parsarium.py afl run runs/xml-github_com_go_forks_go_pkg_xmlx-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
