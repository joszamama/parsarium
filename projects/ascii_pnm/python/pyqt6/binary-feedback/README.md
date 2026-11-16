# PyQt6 native binary feedback pilot

This optional image uses AFL++ QEMU to record edges inside the prebuilt Qt GUI library used by `QImageReader`. It provides binary feedback for a parser binding whose native source cannot be instrumented from the PyQt6 wheel. The main project remains staged for native decoder source coverage.

From the repository root:

```sh
projects/ascii_pnm/python/pyqt6/binary-feedback/run-smoke.sh
```

The script builds the pinned project image and this small AFL++ overlay. It reads a valid PPM and a valid PGM through a Qt byte-stream input. The smoke check discovers the `libQt6Gui.so.6` executable mapping, excludes the Python executable, and runs `afl-showmap -Q` on each control. It requires an identical map on a repeated PPM run, a different map for the PGM, and at most two residual tuples when the Qt mapping is excluded. The [observed result](evidence.json) was 794 PPM tuples, 793 PGM tuples, and one residual tuple.

The executable mapping is discovered at runtime because hard-coded QEMU addresses are not portable. The overlay also contains `afl-fuzz` for a campaign using the reported `module_text_range` as `AFL_QEMU_INST_RANGES`, the reported `executable_excluded_range` as `AFL_QEMU_EXCLUDE_RANGES`, `-Q`, and the `run-once.py` file argument as `@@`. A campaign must set a longer per-execution timeout on hosts that emulate `linux/amd64`.

This is binary edge feedback from the Qt GUI shared object. It is not Qt source-line coverage and does not identify individual PNM decoder functions. The [AFL++ QEMU documentation](https://github.com/AFLplusplus/AFLplusplus/blob/stable/qemu_mode/README.md#7-partial-instrumentation) describes the address-range filters.
