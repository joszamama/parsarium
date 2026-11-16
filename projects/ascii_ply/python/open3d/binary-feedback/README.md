# Open3D PLY reader binary feedback

The pinned Open3D 0.20.0 wheel contains `libOpen3D.so.0.20` (SHA-256 `f0a24df9c2e81e2aba038f191a2bf96a21ce412902ef77018c71c6012a5c932f`). Its exported `open3d::io::ReadTriangleMeshFromPLY` symbol has ELF value `0x40132d0` and size `0x6d7` bytes. The AFL++ QEMU smoke derives the mapped function address from the library's executable mapping and instruments only that function. This provides PLY-reader function feedback; calls made to other functions are outside the measured range. No parser source-line coverage is claimed.

From the repository root:

```sh
projects/ascii_ply/python/open3d/binary-feedback/run-smoke.sh
```

The smoke reads the valid triangle twice and a valid coloured PLY through `open3d.io.read_triangle_mesh(local_path)`. It requires identical maps for repeated triangle input, a different map for the coloured input, and at most two residual tuples when the PLY reader function is excluded. The [observed evidence](evidence.json) records 37 triangle tuples, 38 coloured PLY tuples, and one residual tuple. Each case must finish without timeout and report its geometry result.

The AFL++ overlay includes `afl-fuzz` for a future campaign. Its prepared command uses the observed function range as `AFL_QEMU_INST_RANGES` and the local file argument in `run-once.py` as `@@`. On an emulated `linux/amd64` host, prepare with `--timeout-ms 180000`. The smoke does not run a campaign. Address ranges are tied to the pinned image and are checked against QEMU's runtime map; rebuild and reverify after changing the wheel or platform. See [AFL++ QEMU partial instrumentation](https://github.com/AFLplusplus/AFLplusplus/blob/stable/qemu_mode/README.md#7-partial-instrumentation).
