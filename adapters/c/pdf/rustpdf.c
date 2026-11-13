#include "pdf.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "expected one local PDF path\n");
        return 2;
    }
    FILE *file = fopen(argv[1], "rb");
    if (file == NULL) return 3;
    if (fseek(file, 0, SEEK_END) != 0) return 4;
    long length = ftell(file);
    if (length <= 0) return 5;
    rewind(file);
    uint8_t *bytes = malloc((size_t)length);
    if (bytes == NULL) return 6;
    if (fread(bytes, 1, (size_t)length, file) != (size_t)length) return 7;
    fclose(file);

    uintptr_t pages = 0;
    PdfStatus status = pdf_page_count(bytes, (uintptr_t)length, &pages);
    free(bytes);
    if (status != PDF_STATUS_OK) {
        fprintf(stderr, "%s\n", pdf_last_error_message());
        return 8;
    }
    printf("{\"pages\":%zu}\n", (size_t)pages);
    return 0;
}
