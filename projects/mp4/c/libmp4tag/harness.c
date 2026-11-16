#include "harness.h"
#include <libmp4tag.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parsarium_parse_mp4(const uint8_t *data, size_t size,
                       struct parsarium_mp4_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-libmp4tag-XXXXXX";
    int fd = mkstemp(path);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t count = write(fd, data + offset, size - offset);
        if (count <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)count;
    }
    close(fd);
    int error = 0;
    libmp4tag_t *file = mp4tag_open(path, &error);
    int ok = 0;
    if (file && mp4tag_parse(file) == MP4TAG_OK) {
        mp4tagpub_t title = {0};
        if (mp4tag_get_tag_by_name(file, "\xC2\xA9nam", &title) == MP4TAG_OK &&
            title.data && strlen(title.data) < sizeof(result->title)) {
            strcpy(result->title, title.data);
            result->duration_ms = mp4tag_duration(file);
            ok = 1;
        }
    }
    if (file) mp4tag_free(file);
    unlink(path);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_mp4_result result;
    (void)parsarium_parse_mp4(data, size, &result);
    return 0;
}
