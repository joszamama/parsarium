# Rust × ASCII PNM: verified parser ranking

21 verified third-party crate paths; working goal 20, original ceiling 30. The metric is crates.io crate-level recent downloads over 90 days, captured at 2026-11-12T02:48:59.065626+00:00. It includes all releases of each crate name and is compared only within Rust. 0 crate(s) lack a metric and remain unranked; equal counts share a rank.

Search hits, unresolved leads, and the standard-library inventory are separate from this ranking. See `cell.json`, `leads.json`, and `verification.json` in this directory.

| Rank | Crate | Pinned release | 90-day downloads | Scope | Underlying family |
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
| 11 | [oxideav-pbm](https://docs.rs/oxideav-pbm/0.0.5/oxideav_pbm/decoder/fn.decode_pbm.html) | 0.0.5 | 420 | P3 ASCII PPM RGB pixels | OxideAV PBM decoder |
| 12 | [photocraft](https://docs.rs/photocraft/0.1.2/photocraft/struct.Image.html#method.read_ppm) | 0.1.2 | 132 | P3 ASCII PPM RGB pixels | photocraft PPM reader |
| 13 | [rusty-ppm](https://docs.rs/rusty-ppm/0.3.0/rusty_ppm/ppm_reader/fn.read_ppm.html) | 0.3.0 | 109 | P3 ASCII PPM RGB pixels; compact spacing required by this release | rusty-ppm reader |
| 14 | [opencv-no-c-imgcodecs](https://docs.rs/opencv-no-c-imgcodecs/0.1.0/cv_imgcodecs/pnm/fn.decode.html) | 0.1.0 | 70 | P3 ASCII PPM BGR pixels | opencv-no-c PNM decoder |
| 15 | [pnm](https://docs.rs/pnm/0.1.1/pnm/fn.decode.html) | 0.1.1 | 23 | P3 ASCII PPM RGB pixels; pinned release requires nightly feature | pnm crate decoder |
| 16 | [unicraft](https://docs.rs/unicraft/0.1.2/unicraft/prelude/struct.Image.html#method.read_ppm) | 0.1.2 | 19 | P3 ASCII PPM RGB pixels | unicraft re-export of photocraft PPM reader |
| 17 | [ai-image](https://docs.rs/ai-image/0.25.10/ai_image/fn.load_from_memory_with_format.html) | 0.25.10 | 9 | P3 ASCII PPM RGB pixels | image-rs fork |
| 18 | [roka-qr](https://docs.rs/roka-qr/0.1.1/roka_qr/struct.Reader.html#method.from_pbm) | 0.1.1 | 8 | P1 ASCII PBM QR image and payload | roka-qr P1 bitmap reader plus QR decoder |
| 19 | [imageun](https://docs.rs/imageun/0.0.0/imageun/fn.load_from_memory_with_format.html) | 0.0.0 | 4 | P3 ASCII PPM RGB pixels | image-rs fork |
| 20 | [include-pnm](https://docs.rs/include-pnm/1.0.0/include_pnm/macro.include_ppm.html) | 1.0.0 | 3 | P3 ASCII PPM RGB pixels at compile time | include-pnm compile-time parser |
| 21 | [coldiron](https://docs.rs/coldiron/0.1.0/coldiron/struct.Image.html#method.read_from) | 0.1.0 | 2 | P2 ASCII PGM grayscale pixels | coldiron Netpbm reader |
