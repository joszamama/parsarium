#ifndef PARSARIUM_PDF4QT_H
#define PARSARIUM_PDF4QT_H
#include <cstddef>
#include <cstdint>
bool parsarium_parse_pdf_file(const char *path, std::size_t &pages);
bool parsarium_parse_pdf_bytes(const std::uint8_t *data, std::size_t size, std::size_t &pages);
extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size);
#endif
