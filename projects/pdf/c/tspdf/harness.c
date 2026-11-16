#include "harness.h"
#include <tspdf.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parsarium_parse_pdf(const uint8_t *data, size_t size,
                       struct parsarium_pdf_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-tspdf-XXXXXX";
    int fd = mkstemp(path);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t count = write(fd, data + offset, size - offset);
        if (count <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)count;
    }
    close(fd);
    TspdfError error;
    memset(&error, 0, sizeof(error));
    TspdfReader *document = tspdf_reader_open_file(path, &error);
    int ok = 0;
    if (document) {
        size_t count = tspdf_reader_page_count(document);
        if (count && tspdf_reader_get_page(document, 0)) {
            result->pages = count;
            ok = 1;
        }
        tspdf_reader_destroy(document);
    }
    unlink(path);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_pdf_result result;
    (void)parsarium_parse_pdf(data, size, &result);
    return 0;
}
