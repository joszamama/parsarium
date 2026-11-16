#ifndef PARSARIUM_TSPDF_CPP_HARNESS_H
#define PARSARIUM_TSPDF_CPP_HARNESS_H
#include <cstddef>
#include <cstdint>
struct parsarium_pdf_result { std::size_t pages; };
bool parsarium_parse_pdf(const std::uint8_t *data, std::size_t size,
                         parsarium_pdf_result *result);
#endif
