#include "harness.h"
#include <mupdf/fitz.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parse_data(const uint8_t *data, size_t size, Result *result) {
    if (!data || !result || !size || size > (8u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.pdf";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    fz_context *context = fz_new_context(NULL, NULL, FZ_STORE_UNLIMITED);
    if (!context) { unlink(path); return 0; }
    fz_document *document = NULL;
    fz_var(document);
    int ok = 0;
    fz_try(context) {
        fz_register_document_handlers(context);
        document = fz_open_document(context, path);
        result->pages = fz_count_pages(context, document);
        ok = result->pages > 0;
    } fz_catch(context) {
        ok = 0;
    }
    if (document) fz_drop_document(context, document);
    fz_drop_context(context);
    unlink(path);
    return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    Result result;
    (void)parse_data(data, size, &result);
    return 0;
}
