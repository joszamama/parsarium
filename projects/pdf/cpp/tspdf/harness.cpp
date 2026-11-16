#include "harness.h"
#include <tspdf.h>
#include <cstdlib>
#include <cstring>
#include <unistd.h>

bool parsarium_parse_pdf(const std::uint8_t *data, std::size_t size,
                         parsarium_pdf_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return false;
    *result = {};
    char path[] = "/tmp/parsarium-tspdf-cpp-XXXXXX";
    int fd = mkstemp(path);
    if (fd < 0) return false;
    std::size_t offset = 0;
    while (offset < size) {
        ssize_t count = write(fd, data + offset, size - offset);
        if (count <= 0) { close(fd); unlink(path); return false; }
        offset += static_cast<std::size_t>(count);
    }
    close(fd);
    TspdfError error{};
    TspdfReader *document = tspdf_reader_open_file(path, &error);
    bool ok = false;
    if (document) {
        std::size_t count = tspdf_reader_page_count(document);
        if (count && tspdf_reader_get_page(document, 0)) {
            result->pages = count;
            ok = true;
        }
        tspdf_reader_destroy(document);
    }
    unlink(path);
    return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    parsarium_pdf_result result;
    (void)parsarium_parse_pdf(data, size, &result);
    return 0;
}
