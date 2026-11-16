#include "harness.h"
#include <poppler.h>
#include <string.h>

int parse_data(const uint8_t *data, size_t size, Result *result) {
    if (!data || !result || !size || size > (8u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    GBytes *bytes = g_bytes_new(data, size);
    GError *error = NULL;
    PopplerDocument *document = poppler_document_new_from_bytes(bytes, NULL, &error);
    g_bytes_unref(bytes);
    if (!document) {
        g_clear_error(&error);
        return 0;
    }
    int pages = poppler_document_get_n_pages(document);
    g_object_unref(document);
    if (pages <= 0 || pages > 100000) return 0;
    result->pages = pages;
    return 1;
}
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    Result result;
    (void)parse_data(data, size, &result);
    return 0;
}
