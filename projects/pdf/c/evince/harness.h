#ifndef PARSARIUM_EVINCE_PDF_H
#define PARSARIUM_EVINCE_PDF_H
#include <stddef.h>
#include <stdint.h>
int parsarium_parse_pdf_file(const char *path, int *pages);
int parsarium_parse_pdf_bytes(const uint8_t *data, size_t size, int *pages);
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size);
#endif
