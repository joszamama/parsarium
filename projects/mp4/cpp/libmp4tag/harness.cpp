#include "harness.h"
#include <libmp4tag.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <unistd.h>

bool parsarium_parse_mp4(const std::uint8_t *data, std::size_t size,
                         parsarium_mp4_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return false;
    *result = {};
    char path[] = "/tmp/parsarium-libmp4tag-cpp-XXXXXX";
    int fd = mkstemp(path);
    if (fd < 0) return false;
    std::size_t offset = 0;
    while (offset < size) {
        ssize_t count = write(fd, data + offset, size - offset);
        if (count <= 0) { close(fd); unlink(path); return false; }
        offset += static_cast<std::size_t>(count);
    }
    close(fd);
    int error = 0;
    libmp4tag_t *file = mp4tag_open(path, &error);
    bool ok = false;
    if (file && mp4tag_parse(file) == MP4TAG_OK) {
        mp4tagpub_t title = {};
        if (mp4tag_get_tag_by_name(file, "\xC2\xA9nam", &title) == MP4TAG_OK &&
            title.data && std::strlen(title.data) < sizeof(result->title)) {
            std::strcpy(result->title, title.data);
            result->duration_ms = mp4tag_duration(file);
            ok = true;
        }
    }
    if (file) mp4tag_free(file);
    unlink(path);
    return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    parsarium_mp4_result result;
    (void)parsarium_parse_mp4(data, size, &result);
    return 0;
}
