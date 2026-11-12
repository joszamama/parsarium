use serde_json::json;
use std::env;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        return Err("usage: parsarium-rust-hybit-matrix-market PACKAGE CONTROL.mtx".into());
    }
    let (entries, rows, cols, csr_entries) = match args[1].as_str() {
        "hybit" => {
            let (matrix, info) = hybit::read_matrix_market(&args[2])?;
            (info.input_entries, info.nrows, info.ncols, matrix.nnz())
        }
        "hybit-matrix" => {
            let (matrix, info) = hybit_matrix::read_matrix_market(&args[2])?;
            (info.input_entries, info.nrows, info.ncols, matrix.nnz())
        }
        other => return Err(format!("unknown package: {other}").into()),
    };
    println!("{}", json!({"rows": rows, "cols": cols,
                           "entries": entries, "csr_entries": csr_entries}));
    Ok(())
}
