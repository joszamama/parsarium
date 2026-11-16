# oxvg_ast — SVG / Rust

Pinned release: `0.0.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/oxvg-ast/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust oxvg_ast
python3 parsarium.py run svg rust oxvg_ast controls/svg/red-green.svg
python3 parsarium.py replay svg rust oxvg_ast CORPUS_DIR runs/svg-oxvg_ast-replay
python3 parsarium.py afl build svg rust oxvg_ast
python3 parsarium.py afl prepare svg rust oxvg_ast runs/svg-oxvg_ast-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
