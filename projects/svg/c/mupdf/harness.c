#include "harness.h"
#include <mupdf/fitz.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parse_data(const uint8_t *data, size_t size, Result *result) {
    if (!data || !result || !size || size > (8u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.svg";
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
    fz_page *page = NULL;
    fz_pixmap *image = NULL;
    fz_var(document);
    fz_var(page);
    fz_var(image);
    int ok = 0;
    fz_try(context) {
        fz_register_document_handlers(context);
        document = fz_open_document(context, path);
        if (fz_count_pages(context, document) > 0) {
            page = fz_load_page(context, document, 0);
            image = fz_new_pixmap_from_page(context, page, fz_identity,
                                            fz_device_rgb(context), 0);
            if (image && image->w >= 2 && image->h >= 1 && image->n == 3) {
                result->width = image->w;
                result->height = image->h;
                memcpy(result->first, image->samples, 3);
                memcpy(result->second, image->samples + 3, 3);
                ok = 1;
            }
        }
    } fz_catch(context) {
        ok = 0;
    }
    if (image) fz_drop_pixmap(context, image);
    if (page) fz_drop_page(context, page);
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
