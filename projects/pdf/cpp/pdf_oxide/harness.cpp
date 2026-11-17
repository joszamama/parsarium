#include "harness.h"
#include <pdf_oxide/pdf_oxide.hpp>
#include <vector>

namespace {
constexpr std::size_t kMaxInput = 1u << 20;
}  // namespace

bool parsarium_parse_pdf(const std::uint8_t *data, std::size_t size, int &pages) {
    pages = -1;
    if (!data || !size || size > kMaxInput) return false;
    // The tagged C++17 facade takes an owned byte vector and forwards it to
    // pdf_document_open_from_bytes; the Document destructor frees the handle.
    std::vector<std::uint8_t> bytes(data, data + size);
    try {
        auto document = pdf_oxide::Document::open_from_bytes(bytes);
        pages = document.page_count();
    } catch (const pdf_oxide::Error &) {
        pages = -1;
        return false;
    }
    return pages >= 0;
}
