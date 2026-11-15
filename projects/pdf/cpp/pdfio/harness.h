#ifndef PARSARIUM_PDFIO_HARNESS_H
#define PARSARIUM_PDFIO_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_pdf_result { size_t pages; };
int parsarium_parse_pdf(const uint8_t *data,size_t size,struct parsarium_pdf_result *result);
#endif
