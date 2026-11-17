# PyQt5 native binary feedback

The pinned PyQt5 5.15.11 wheel uses Qt 5.15.19. AFL++ QEMU observes executable edges in its `libQt5Gui.so.5` shared library while `QImageReader` reads a valid ASCII P3 image. This provides native library feedback, with no claim of Qt source-line coverage or individual PNM decoder-function attribution. PyQt5 and PyQt6 share the Qt PPM parser family, but use separately pinned Qt major versions.

From the repository root:

```sh
projects/ascii_pnm/python/pyqt5/binary-feedback/run-smoke.sh
```

The script builds the pinned project and AFL++ overlay, reads the valid red/green PPM twice, then reads the valid black/white PGM. It discovers the Qt GUI executable mapping at runtime and limits AFL QEMU instrumentation to that mapping. Passing requires a stable map for repeated PPM input, a different map for PGM, and at most two residual tuples when Qt GUI is excluded. The [observed evidence](evidence.json) records 842 PPM tuples, 835 PGM tuples, and one residual tuple.

The overlay also includes `afl-fuzz` for a future campaign. Use its reported `module_text_range` for `AFL_QEMU_INST_RANGES`, `executable_excluded_range` for `AFL_QEMU_EXCLUDE_RANGES`, `-Q`, and the local file argument in `run-once.py` as `@@`. A campaign should set a timeout suitable for the host's `linux/amd64` emulation. The smoke check does not run a campaign.
