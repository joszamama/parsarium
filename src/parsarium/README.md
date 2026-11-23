# Parsarium

An open testbed of real parsers: 1,163 open-source parser packages for 16 file formats and protocols (PNG, ZIP, MP4, WAV, PDF, SVG, HTTP/1.1, ASCII PLY, ASCII PNM, MP3, JSON, XML, YAML, TOML, SQL and DNS messages) in C, C++, Go, Java, JavaScript, Python, Rust and PHP. Each target has a pinned release, a documented input API, a Docker harness checked against valid control files, and an AFL++ overlay, and can be fed inputs that Fandango generates from the format's grammar.

Website, atlas, and manual: [parsarium.com](https://parsarium.com)

## Install

```sh
pip install parsarium
```

Requires Python 3.11+ and Docker for running targets. Release wheels include this version's snapshot. The first command that needs targets checks its SHA-256 and extracts it into your cache directory without a network download. Each package version pins one snapshot, so a version identifies an exact set of targets.

## Use

```sh
parsarium list --format png
parsarium show png c lodepng
parsarium run png c lodepng my.png --results runs/lodepng
parsarium run-format png --file my.png --results runs/png-my-file
parsarium fandango setup
parsarium afl build png c lodepng
parsarium afl prepare png c lodepng runs/lodepng-afl --fandango 100
parsarium afl run runs/lodepng-afl --seconds 3600
parsarium fandango generate png c lodepng runs/lodepng-fandango --count 100 --seed 42 --replay --prepare-afl
parsarium afl run runs/lodepng-fandango/afl --check
```

`afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec; `plan.json` records the spec, its SHA-256, the random seed (`--fandango-seed`, default 42) and the Fandango version. Without it, the control is the only seed. `native prepare` takes the same option.

Run a selection saved from the [bench](https://parsarium.com/bench/):

```sh
parsarium run-selection sel-90378f4e58.json --mode control
parsarium run-selection sel-90378f4e58.json --mode afl --seconds 600 --count 100
parsarium run-selection sel-90378f4e58.json --mode fandango --count 100 --seed 42
```

`parsarium home` shows where the snapshot lives. Set `PARSARIUM_HOME` to a clone of the repository to use it instead of the bundled snapshot.

## Python

```python
from parsarium import catalog

for t in catalog.targets(format="png", ecosystem="rust"):
    print(t.id, t.package, t.release, t.family, t.input_api)
```

## License

Apache-2.0. Each parser keeps its own license, recorded in the catalog. Please read the [ethics and responsible-use notes](https://github.com/joszamama/parsarium/blob/main/ETHICS.md) before publishing findings.

## Citing

Cite the package version (or the repository commit) you used, and the selection ID if you used a subset. See [parsarium.com/about](https://parsarium.com/about/#cite).
