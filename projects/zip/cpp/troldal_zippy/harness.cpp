#include "harness.h"
#include <Zippy.hpp>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <unistd.h>

int parsarium_parse_zip(const uint8_t *data, size_t size,
                        parsarium_zip_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    *result = {};
    char path[] = "/tmp/parsarium-zippy-XXXXXX";
    int fd = mkstemp(path);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t count = write(fd, data + offset, size - offset);
        if (count <= 0) { close(fd); unlink(path); return 0; }
        offset += static_cast<size_t>(count);
    }
    close(fd);
    int ok = 0;
    try {
        Zippy::ZipArchive archive;
        archive.Open(path);
        const auto names = archive.GetEntryNames();
        if (!names.empty()) {
            const std::string content = archive.GetEntry(names[0]).GetDataAsString();
            if (names[0].size() < sizeof(result->name) &&
                content.size() <= sizeof(result->content)) {
                result->entries = names.size();
                result->name_len = names[0].size();
                std::memcpy(result->name, names[0].data(), result->name_len);
                result->content_len = content.size();
                std::memcpy(result->content, content.data(), result->content_len);
                ok = 1;
            }
        }
        archive.Close();
    } catch (...) { ok = 0; }
    unlink(path);
    return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    parsarium_zip_result result;
    (void)parsarium_parse_zip(data, size, &result);
    return 0;
}
