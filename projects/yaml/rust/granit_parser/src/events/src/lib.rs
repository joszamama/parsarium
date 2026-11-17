//! Monomorphization shim: granit_parser::Parser<StrInput> is generic, so its code is compiled into the
//! crate that instantiates it. This crate holds only that instantiation, letting the AFL++
//! overlay instrument the parser code without instrumenting the harness's tree builder.

pub use granit_parser::{Event, ScalarStyle, ScanError};

/// Drain granit_parser::Parser::new_from_str into its events.
pub fn events(text: &str) -> Result<Vec<Event<'_>>, ScanError> {
    granit_parser::Parser::new_from_str(text).map(|item| item.map(|(event, _span)| event)).collect()
}
