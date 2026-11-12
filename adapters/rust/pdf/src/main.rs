use std::error::Error;
use std::path::Path;

fn parse(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let result = match package {
        "lopdf" => {
            let document = lopdf::Document::load(path)?;
            serde_json::json!({"pages":document.get_pages().len()})
        }
        "pdf-extract" => {
            let text = pdf_extract::extract_text(path)?;
            serde_json::json!({"has_parsarium":text.contains("Parsarium")})
        }
        "printpdf" => {
            let bytes = std::fs::read(path)?;
            let mut warnings = Vec::new();
            let document = printpdf::PdfDocument::parse(&bytes, &printpdf::PdfParseOptions::default(), &mut warnings)
                .map_err(|error| format!("{error}"))?;
            serde_json::json!({"pages":document.pages.len()})
        }
        "pdf-inspector" => {
            let result = pdf_inspector::process_pdf(path)?;
            serde_json::json!({"pages":result.page_count,"title":result.title})
        }
        "pdf_oxide" => {
            let document = pdf_oxide::PdfDocument::open(path)?;
            serde_json::json!({"pages":document.page_count()?})
        }
        "oxidize-pdf" => {
            let document = oxidize_pdf::PdfDocument::open(path)?;
            serde_json::json!({"pages":document.page_count()?})
        }
        "pdf" => {
            let document = pdf::file::FileOptions::cached().open(path)?;
            serde_json::json!({"pages":document.num_pages()})
        }
        "pdf-text-extract" => {
            let bytes = std::fs::read(path)?;
            let mut document = pdf_text_extract::Document::parse(&bytes)?;
            serde_json::json!({"pages":document.page_count()?})
        }
        "pdfsink-rs" => {
            let document = pdfsink_rs::PdfDocument::open(path)?;
            serde_json::json!({"pages":document.len()})
        }
        "pdfpurr" => {
            let document = pdfpurr::Document::open(path)?;
            serde_json::json!({"pages":document.page_count()?})
        }
        "pdf-cos" => {
            let document = pdf_cos::Document::load(path)?;
            serde_json::json!({"pages":document.get_pages().len()})
        }
        "pdfrum" => {
            let document = pdfrum::Document::open(path)?;
            serde_json::json!({"pages":document.page_count()})
        }
        "pdfrum-parser" => {
            let bytes = std::fs::read(path)?;
            let document = pdfrum_parser::load(std::sync::Arc::from(bytes), &pdfrum_parser::LoadOptions::default())?;
            serde_json::json!({"pages":document.page_count()})
        }
        "zpdf" => {
            let bytes = std::fs::read(path)?;
            let document = zpdf::PdfDocument::open(bytes)?;
            serde_json::json!({"pages":document.page_count()})
        }
        "zpdf-document" => {
            let bytes = std::fs::read(path)?;
            let document = zpdf_document::PdfDocument::open(bytes)?;
            serde_json::json!({"pages":document.page_count()})
        }
        "pdfboss-core" => {
            let document = pdfboss_core::Document::open(path)?;
            serde_json::json!({"pages":document.page_count()})
        }
        "unpdf" => {
            let document = unpdf::parse_file(path)?;
            serde_json::json!({"pages":document.page_count()})
        }
        "pdfer_forms" => {
            let document = pdfer_forms::PdfReaderCompat::load(path)?;
            serde_json::json!({"pages":document.pages().len()})
        }
        "pdfplumber" => {
            let document = pdfplumber::Pdf::open_path(path, None)?;
            serde_json::json!({"pages":document.page_count()})
        }
        "pdf-syntax" => {
            let bytes = std::fs::read(path)?;
            let document = pdf_syntax::Pdf::new(std::sync::Arc::new(bytes))
                .map_err(|error| format!("{error:?}"))?;
            serde_json::json!({"pages":document.pages().len()})
        }
        "flpdf" => {
            let mut document = flpdf::Pdf::open(std::fs::File::open(path)?)?;
            let pages = flpdf::PageDocumentHelper::new(&mut document).get_all_pages()?;
            serde_json::json!({"pages":pages.len()})
        }
        _ => return Err(format!("unknown package: {package}").into()),
    };
    Ok(result)
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = std::env::args_os().skip(1);
    let package = args.next().ok_or("usage: adapter PACKAGE CONTROL")?;
    let path = args.next().ok_or("usage: adapter PACKAGE CONTROL")?;
    if args.next().is_some() { return Err("usage: adapter PACKAGE CONTROL".into()); }
    let package = package.to_str().ok_or("package must be UTF-8")?;
    println!("{}", parse(package, Path::new(&path))?);
    Ok(())
}
