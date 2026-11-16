#include "harness.h"
#include <qpdf/qpdf-c.h>
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
    qpdf_data pdf = qpdf_init();
    int ok = 0;
    if (pdf) {
        if ((qpdf_read(pdf, path, NULL) & QPDF_ERRORS) == 0) {
            result->pages = qpdf_get_num_pages(pdf);
            ok = result->pages > 0;
        }
        qpdf_cleanup(&pdf);
    }
    unlink(path);
    return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    Result result;
    (void)parse_data(data, size, &result);
    return 0;
}
