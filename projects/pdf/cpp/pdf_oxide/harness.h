#ifndef PARSARIUM_PDF_OXIDE_CPP_HARNESS_H
#define PARSARIUM_PDF_OXIDE_CPP_HARNESS_H
#include <cstddef>
#include <cstdint>

// Parses one PDF through pdf_oxide::Document::open_from_bytes and reads
// page_count(). Returns false unless the Rust engine reported a page count.
bool parsarium_parse_pdf(const std::uint8_t *data, std::size_t size, int &pages);
#endif
