#include "harness.h"
#include <InputFile.h>
#include <PDFParser.h>
#include <cstring>
#include <exception>
#include <unistd.h>

// Inputs above 1 MiB are rejected to match the Parsarium corpus bridge.
bool parse_data(const std::uint8_t *data, std::size_t size, Result *result) {
    if (!data || !result || !size || size > (1u << 20)) return false;
    std::memset(result, 0, sizeof(*result));
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
    try {
        // The file outlives the parser, which reads through its stream.
        InputFile file;
        if (file.OpenFile(path) == PDFHummus::eSuccess) {
            PDFParser parser;
            if (parser.StartPDFParsing(file.GetInputStream()) == PDFHummus::eSuccess) {
                const unsigned long pages = parser.GetPagesCount();
                if (pages <= 0x7fffffffUL) {
                    result->pages = static_cast<int>(pages);
                    ok = true;
                }
            }
        }
    } catch (const std::exception&) {
        ok = false;
    }
    unlink(path);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    Result result{};
    (void)parse_data(data, size, &result);
    return 0;
}
