//! Monomorphization shim: saphyr's YamlLoader<Yaml> and saphyr_parser::Parser is generic, so its code is compiled into the
//! crate that instantiates it. This crate holds only that instantiation, letting the AFL++
//! overlay instrument the parser code without instrumenting the harness's tree builder.

pub use saphyr::{Scalar, ScanError, Yaml};
use saphyr::LoadableYamlNode;

/// Load all documents with saphyr's Yaml::load_from_str.
pub fn load(text: &str) -> Result<Vec<Yaml<'_>>, ScanError> {
    Yaml::load_from_str(text)
}
