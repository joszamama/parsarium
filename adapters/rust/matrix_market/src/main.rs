use serde_json::json;
use std::{env, fs, io::Cursor};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        return Err("usage: parsarium-rust-matrix-market PACKAGE CONTROL.mtx".into());
    }
    let path = &args[2];
    let bytes = if args[1] == "kira-scio" { Vec::new() } else { fs::read(path)? };
    let output = match args[1].as_str() {
        "sprs" => {
            let matrix: sprs::TriMatI<f64, usize> = sprs::io::read_matrix_market(path)?;
            json!({"rows": matrix.shape().0, "cols": matrix.shape().1, "entries": matrix.nnz()})
        }
        "matrix-market-rs" => {
            use matrix_market_rs::MtxData;
            let matrix: MtxData<f64> = MtxData::from_file(path)?;
            match matrix {
                MtxData::Sparse(shape, positions, values, _) =>
                    json!({"rows": shape[0], "cols": shape[1], "entries": values.len(),
                           "first_position": positions[0], "first_value": values[0]}),
                MtxData::Dense(shape, values, _) =>
                    json!({"rows": shape[0], "cols": shape[1], "entries": values.len(),
                           "first_value": values[0]}),
            }
        }
        "matrix_merchant" => {
            use matrix_merchant::reader::MtxReader;
            let reader = MtxReader::new_reader(Cursor::new(&bytes))?;
            let mut coordinates = reader.matrix().ok_or("not a matrix")?
                .coordinate().ok_or("not coordinate storage")?;
            let shape = coordinates.size();
            let mut entries = 0;
            let mut first = None;
            for item in &mut coordinates {
                let (position, value) = item?;
                if first.is_none() { first = Some(json!({"row": position.row,
                                                       "col": position.col,
                                                       "value": format!("{value:?}")})); }
                entries += 1;
            }
            json!({"rows": shape.num_rows, "cols": shape.num_cols,
                   "entries": entries, "first": first})
        }
        "sci-io" => {
            let info = sci_io::mminfo(Cursor::new(&bytes))?;
            let matrix = sci_io::mmread(Cursor::new(&bytes))?;
            let kind = match matrix {
                sci_io::MarketMatrix::Sparse(_) => "sparse",
                sci_io::MarketMatrix::Dense { .. } => "dense",
            };
            json!({"rows": info.rows, "cols": info.cols,
                   "entries": info.entries, "kind": kind})
        }
        "fsci-io" => {
            let content = std::str::from_utf8(&bytes)?;
            let matrix = fsci_io::mmread(content)?;
            json!({"rows": matrix.rows, "cols": matrix.cols,
                   "entries": matrix.info.nnz, "first_value": matrix.data[0]})
        }
        "nalgebra" => {
            let matrix = nalgebra::io::cs_matrix_from_matrix_market::<f64, _>(path)
                .ok_or("nalgebra Matrix Market parse returned None")?;
            json!({"rows": matrix.nrows(), "cols": matrix.ncols()})
        }
        "powerio-matrix" => {
            let matrix = powerio_matrix::io::read_mtx(path)?;
            json!({"rows": matrix.rows(), "cols": matrix.cols(), "entries": matrix.nnz()})
        }
        "feral" => {
            let matrix = feral::io::mtx::read_mtx(std::path::Path::new(path))?;
            json!({"rows": matrix.n, "cols": matrix.n, "entries": matrix.entries.len(),
                   "first_value": matrix.entries[0].2})
        }
        "oxiblas-sparse" => {
            let matrix = oxiblas_sparse::mtx::read_matrix_market::<f64, _>(path)?;
            json!({"rows": matrix.nrows(), "cols": matrix.ncols(), "entries": matrix.nnz()})
        }
        "russell_sparse" => {
            let (real, _complex) = russell_sparse::read_matrix_market(
                path.as_str(), russell_sparse::MMsym::LeaveAsLower)?;
            let matrix = real.ok_or("no real matrix")?;
            let (rows, cols, entries, _) = matrix.get_info();
            json!({"rows": rows, "cols": cols, "entries": entries})
        }
        "scirs2-io" => {
            let matrix = scirs2_io::matrix_market::read_sparse_matrix(path)?;
            json!({"rows": matrix.rows, "cols": matrix.cols, "entries": matrix.nnz})
        }
        "legume-numeric" => {
            let (triplets, (rows, cols, declared)) =
                legume_numeric::matrix::mtx_io::read_mtx_triplets(path)?;
            json!({"rows": rows, "cols": cols, "entries": triplets.len(),
                   "declared": declared, "first_value": triplets[0].2})
        }
        "cyanea-omics" => {
            let matrix = cyanea_omics::sc_mtx::read_mtx(std::str::from_utf8(&bytes)?)?;
            json!({"rows": matrix.shape().0, "cols": matrix.shape().1,
                   "entries": matrix.nnz(), "first_value": matrix.get(0, 0)})
        }
        "rma" => {
            use rma::cuthill_mckee::{MatrixMarketMatrix, MtxType};
            let matrix = rma::cuthill_mckee::read_matrix_market(path, MtxType::Csr)?;
            let MatrixMarketMatrix::Csr(matrix) = matrix else { return Err("expected CSR".into()) };
            json!({"rows": matrix.nrows, "cols": matrix.ncols,
                   "entries": matrix.indices.len(),
                   "first_value": matrix.data.as_ref().map(|values| values[0])})
        }
        "kira-scio" => {
            let matrix = kira_scio::formats::mtx10x::read_matrix(std::path::Path::new(path), true)?;
            json!({"rows": matrix.n_genes, "cols": matrix.n_cells,
                   "entries": matrix.values.len(), "first_value": matrix.values[0]})
        }
        "rlst" => {
            use rlst::{Nonzeros, Shape};
            let matrix = rlst::io::matrix_market::read_coordinate_mm::<f64>(path)?;
            let shape = matrix.shape();
            json!({"rows": shape[0], "cols": shape[1], "entries": matrix.nnz()})
        }
        "rivrs-sparse" => {
            let matrix = rivrs_sparse::io::mtx::load_mtx(std::path::Path::new(path))?;
            json!({"rows": matrix.nrows(), "cols": matrix.ncols()})
        }
        "ls_solver" => {
            let matrix = ls_solver::api::read_matrix_from_matrix_market_file(path);
            json!({"rows": matrix.nrows(), "cols": matrix.ncols(), "entries": matrix.nnz()})
        }
        other => return Err(format!("unknown package: {other}").into()),
    };
    println!("{output}");
    Ok(())
}
