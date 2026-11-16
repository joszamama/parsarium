# PySide6 native binary feedback pilot

From the repository root, run `projects/ascii_pnm/python/pyside6/binary-feedback/run-smoke.sh`. The script builds the pinned PySide6 image and AFL++ QEMU overlay, parses valid PPM and PGM byte streams, and discovers the executable mapping of `libQt6Gui.so.6` at runtime.

The [observed result](evidence.json) was 733 Qt GUI binary tuples for PPM and 732 for PGM. Repeating the PPM produced the same map; excluding Qt GUI left one residual tuple. This is library-level binary feedback, not native source-line coverage or per-decoder function attribution. The Qt GUI binary is byte-identical to the one in the PyQt6 6.12.0 wheel.

The [receipt rule](../../../../ascii_pnm/python/pyqt6/binary-feedback/receipt-rule.md) defines how this mode may be audited. The project remains staged until the shared audit accepts the binary receipt.
