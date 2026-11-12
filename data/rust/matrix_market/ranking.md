# Rust × Matrix Market: verified parser ranking

20 verified third-party crate paths; working goal 20, original ceiling 30. The metric is crates.io crate-level recent downloads over 90 days, captured at 2026-11-12T03:07:14.807854+00:00. It includes all releases of each crate name and is compared only within Rust. 0 crate(s) lack a metric and remain unranked; equal counts share a rank.

Search hits, unresolved leads, and the standard-library inventory are separate from this ranking. See `cell.json`, `leads.json`, and `verification.json` in this directory.

| Rank | Crate | Pinned release | 90-day downloads | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [nalgebra](https://docs.rs/nalgebra/0.35.0/nalgebra/io/fn.cs_matrix_from_matrix_market.html) | 0.35.0 | 17,908,263 | coordinate real general, sparse matrix shape | nalgebra pest Matrix Market grammar |
| 2 | [sprs](https://docs.rs/sprs/0.11.6/sprs/io/fn.read_matrix_market.html) | 0.11.6 | 2,500,034 | coordinate real general, shape and triplet count | sprs Matrix Market parser |
| 3 | [feral](https://docs.rs/feral/0.22.0/feral/io/mtx/fn.read_mtx.html) | 0.22.0 | 27,502 | coordinate real symmetric, lower triangle entries | feral own symmetric MTX parser |
| 4 | [oxiblas-sparse](https://docs.rs/oxiblas-sparse/0.2.3/oxiblas_sparse/mtx/fn.read_matrix_market.html) | 0.2.3 | 9,013 | coordinate real general, CSR shape and entries | oxiblas-sparse own MTX parser |
| 5 | [powerio-matrix](https://docs.rs/powerio-matrix/0.11.11/powerio_matrix/io/mtx/fn.read_mtx.html) | 0.11.11 | 7,830 | coordinate real general, CSR shape and entries | powerio-matrix wrapper over sprs |
| 6 | [matrix-market-rs](https://docs.rs/matrix-market-rs/0.1.3/matrix_market_rs/enum.MtxData.html#method.from_file) | 0.1.3 | 5,869 | coordinate real general, positions and values | matrix-market-rs own parser |
| 7 | [legume-numeric](https://docs.rs/legume-numeric/0.9.8/legume_numeric/matrix/mtx_io/fn.read_mtx_triplets.html) | 0.9.8 | 2,691 | coordinate real general, triplets and shape | legume-numeric MTX triplet reader |
| 8 | [rlst](https://docs.rs/rlst/0.12.0/rlst/io/matrix_market/fn.read_coordinate_mm.html) | 0.12.0 | 2,339 | coordinate real general, CSR shape and entries | rlst own Matrix Market reader |
| 9 | [russell_sparse](https://docs.rs/russell_sparse/5.1.0/russell_sparse/fn.read_matrix_market.html) | 5.1.0 | 1,937 | coordinate real general, COO shape and entries | russell_sparse own Matrix Market parser |
| 10 | [scirs2-io](https://docs.rs/scirs2-io/0.6.5/scirs2_io/matrix_market/fn.read_sparse_matrix.html) | 0.6.5 | 749 | coordinate real general, shape and entries | scirs2-io own Matrix Market parser |
| 11 | [rivrs-sparse](https://docs.rs/rivrs-sparse/0.1.1/rivrs_sparse/io/mtx/fn.load_mtx.html) | 0.1.1 | 465 | coordinate real symmetric, sparse matrix shape | rivrs-sparse own symmetric MTX reader |
| 12 | [kira-scio](https://docs.rs/kira-scio/0.2.1/kira_scio/formats/mtx10x/fn.read_matrix.html) | 0.2.1 | 351 | 10x Matrix Market directory, integer counts and CSC shape | kira-scio 10x MTX reader |
| 13 | [hybit-matrix](https://docs.rs/hybit-matrix/0.9.0/hybit_matrix/fn.read_matrix_market.html) | 0.9.0 | 165 | coordinate real general, CSR shape and entries | hybit-matrix parser also exposed by hybit |
| 14 | [fsci-io](https://docs.rs/fsci-io/0.4.0/fsci_io/fn.mmread.html) | 0.4.0 | 74 | coordinate real general, dense values | fsci-io own Matrix Market reader |
| 15 | [hybit](https://docs.rs/hybit/0.9.0/hybit/fn.read_matrix_market.html) | 0.9.0 | 63 | coordinate real general, CSR shape and entries | hybit re-export of hybit-matrix parser |
| 16 | [cyanea-omics](https://docs.rs/crate/cyanea-omics/0.1.1/source/src/sc_mtx.rs) | 0.1.1 | 38 | coordinate real general, CSC shape and entries | cyanea-omics MTX parser |
| 17 | [sci-io](https://docs.rs/sci-io/0.1.0/sci_io/fn.mmread.html) | 0.1.0 | 11 | coordinate real general, sparse matrix plus header fields | sci-io Matrix Market reader using sci-sparse storage |
| 18 | [matrix_merchant](https://docs.rs/matrix_merchant/0.1.2/matrix_merchant/reader/enum.MtxReader.html#method.new_reader) | 0.1.2 | 3 | coordinate real general, shape and entries | matrix_merchant own parser |
| 18 | [rma](https://docs.rs/rma/0.4.0/rma/cuthill_mckee/fn.read_matrix_market.html) | 0.4.0 | 3 | coordinate real symmetric, CSR shape and entries | rma symmetric Matrix Market reader |
| 20 | [ls_solver](https://docs.rs/ls_solver/0.1.0/ls_solver/api/fn.read_matrix_from_matrix_market_file.html) | 0.1.0 | 2 | coordinate real general, CSR shape and entries | ls_solver own Matrix Market loader |
