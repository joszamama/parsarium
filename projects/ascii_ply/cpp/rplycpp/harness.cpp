#include "harness.h"
#include "rplycpp.hpp"
#include <vector>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
int parsarium_parse_ply(const uint8_t *data, size_t size, struct parsarium_ply_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.ply";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    rplycpp::PLYReader reader;
    bool ok = reader.Open(path);
    if (!ok) { unlink(path); return 0; }
    std::vector<rplycpp::PLYReadHandler> handlers;
    for (const auto& element : reader.GetElements()) {
        if (element.GetName() == "vertex") {
            handlers.emplace_back([&](const std::vector<double>& values) { if (values.size() >= 3) ++result->vertices; });
        } else if (element.GetName() == "face") {
            handlers.emplace_back([&](const std::vector<double>& values) {
                if (values.size() == 4 && values[0] == 3) {
                    ++result->faces;
                    for (int i = 0; i < 3; i++) result->face[i] = static_cast<long>(values[i + 1]);
                }
            });
        } else handlers.emplace_back(rplycpp::DEFAULT_HANDLER);
    }
    ok = reader.Read(handlers) && reader.Close();
    unlink(path);
    return ok && result->vertices == 3 && result->faces == 1;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_ply_result result; (void)parsarium_parse_ply(data, size, &result); return 0;
}
