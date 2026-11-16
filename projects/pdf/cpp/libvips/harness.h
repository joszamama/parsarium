#ifndef PARSARIUM_VIPS_PDF_HARNESS_H
#define PARSARIUM_VIPS_PDF_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_pdf_result { unsigned pages, width, height; };
int parsarium_parse_pdf(const uint8_t *, size_t, struct parsarium_pdf_result *);
#endif
