#include "harness.h"
#include <poppler-document.h>
#include <poppler-global.h>
#include <cstring>
#include <memory>
#include <string>
#include <unistd.h>

namespace {
void quiet(const std::string &, void *) {}
}

bool parse_data(const std::uint8_t *data, std::size_t size, Result *result) {
    if (!data || !result || !size || size > (8u << 20)) return false;
    std::memset(result, 0, sizeof(*result));
    poppler::set_debug_error_function(quiet, nullptr);
    char path[] = "/tmp/parsarium-XXXXXX.pdf";
    int fd = mkstemps(path, 4);
    if (fd < 0) return false;
    std::size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return false; }
        offset += static_cast<std::size_t>(n);
    }
    close(fd);
    bool ok = false;
    {
        std::unique_ptr<poppler::document> pdf(poppler::document::load_from_file(path));
        if (pdf && !pdf->is_locked()) {
            const int pages = pdf->pages();
            if (pages > 0 && pages <= 100000) {
                result->pages = pages;
                ok = true;
            }
        }
    }
    unlink(path);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    Result result{};
    (void)parse_data(data, size, &result);
    return 0;
}
