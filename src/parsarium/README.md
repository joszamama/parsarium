# Parsarium

An open testbed of real parsers. Parsarium collects open-source packages and standard-library APIs that parse ten formats (PNG, ZIP, MP4, WAV, PDF, SVG, HTTP/1.1, ASCII PLY, ASCII PNM, MP3 + ID3v2) in eight languages (C, C++, Go, Java, JavaScript, Python, Rust, PHP). Each runnable target has a pinned release, a documented input API, a valid control file, a Docker harness, and an AFL++ overlay.

Website, atlas, and manual: [parsarium.com](https://parsarium.com)

## Install

```sh
pip install parsarium
```

Requires Python 3.11+ and Docker for running targets. The first command that needs targets downloads this version's snapshot (about 19 MB) into your cache directory and checks its SHA-256. Each package version pins one snapshot, so a version identifies an exact set of targets.

## Use

```sh
parsarium list --format png
parsarium show png c libpng
parsarium run png c libpng my.png --results runs/libpng
parsarium run-format png --file my.png --results runs/png-my-file
parsarium afl build png c libpng
parsarium afl prepare png c libpng runs/libpng-afl
parsarium afl run runs/libpng-afl --seconds 3600
```

Run a selection saved from the [bench](https://parsarium.com/bench/):

```sh
parsarium run-selection sel-90378f4e58.json --mode control
parsarium run-selection sel-90378f4e58.json --mode afl --seconds 600
```

`parsarium home` shows where the snapshot lives. Set `PARSARIUM_HOME` to a clone of the repository to use it instead of the download.

## Python

```python
from parsarium import catalog

for t in catalog.targets(format="png", ecosystem="rust"):
    print(t.id, t.package, t.release, t.family, t.input_api)
```

## License

Apache-2.0.

## Citing

Cite the package version (or the repository commit) you used, and the selection ID if you used a subset. See [parsarium.com/about](https://parsarium.com/about/#cite).
