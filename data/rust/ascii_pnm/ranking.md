# RUST × ASCII PNM: selected parsers

10 control-verified third-party paths selected from 21 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

crates.io recent downloads (90 days).

| Rank | Package | Release | crates.io downloads (90 days) | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [image](https://docs.rs/image/0.25.10/image/fn.load_from_memory_with_format.html) | 0.25.10 | 79,503,423 | P3 ASCII PPM RGB pixels | image-rs PNM decoder |
| 2 | [imagesize](https://docs.rs/imagesize/0.15.0/imagesize/fn.blob_size.html) | 0.15.0 | 20,457,593 | P3 ASCII PPM header dimensions only; raster samples are not decoded | imagesize PNM header reader |
| 3 | [bevy](https://docs.rs/bevy/0.20.1/bevy/image/struct.Image.html#method.from_buffer) | 0.20.1 | 2,052,137 | P3 ASCII PPM expanded RGBA pixels | Bevy re-export of bevy_image over image-rs PNM |
| 4 | [bevy_image](https://docs.rs/bevy_image/0.20.1/bevy_image/struct.Image.html#method.from_buffer) | 0.20.1 | 1,523,101 | P3 ASCII PPM expanded RGBA pixels | Bevy image wrapper over image-rs PNM |
| 5 | [fltk](https://docs.rs/fltk/1.5.23/fltk/image/struct.PnmImage.html#method.load) | 1.5.23 | 66,810 | P3 ASCII PPM RGB pixels | FLTK C++ PNM image loader |
| 6 | [devela](https://docs.rs/devela/0.30.0/devela/media/visual/image/format/struct.Pnm.html) | 0.30.0 | 2,538 | P3 ASCII PPM RGB pixels | devela PNM decoder |
| 7 | [zenbitmaps](https://docs.rs/zenbitmaps/0.1.5/zenbitmaps/fn.decode.html) | 0.1.5 | 1,577 | P3 ASCII PPM RGB pixels | zenbitmaps PNM decoder |
| 8 | [oxideav-image](https://docs.rs/oxideav-image/0.0.7/oxideav_image/fn.decode_bytes.html) | 0.0.7 | 748 | P3 ASCII PPM RGB pixels | OxideAV image gateway over oxideav-pbm |
| 9 | [oxideav-io](https://docs.rs/oxideav-io/0.1.2/oxideav_io/fn.open_image_with.html) | 0.1.2 | 633 | P3 ASCII PPM RGB pixels | OxideAV I/O gateway over oxideav-image and oxideav-pbm |
| 10 | [libviprs](https://docs.rs/libviprs/0.6.1/libviprs/raster/struct.Raster.html#method.ppm_load) | 0.6.1 | 504 | P3 ASCII PPM RGB pixels | libviprs Netpbm decoder |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
