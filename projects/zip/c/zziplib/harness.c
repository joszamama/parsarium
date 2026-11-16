#include "harness.h"
#include <zzip/zzip.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

int parsarium_parse_zip(const uint8_t *data, size_t size,
                        struct parsarium_zip_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-zzip-XXXXXX";
    int fd = mkstemp(path);
    if (fd < 0) return 0;
    size_t written = 0;
    while (written < size) {
        ssize_t n = write(fd, data + written, size - written);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        written += (size_t)n;
    }
    close(fd);
    zzip_error_t error = (zzip_error_t)0;
    ZZIP_DIR *archive = zzip_dir_open(path, &error);
    unlink(path);
    if (!archive) return 0;
    int ok = 0;
    ZZIP_DIRENT *entry = zzip_readdir(archive);
    if (!entry || !entry->d_name || entry->st_size > sizeof(result->content)) goto done;
    result->name_len = strlen(entry->d_name);
    if (!result->name_len || result->name_len >= sizeof(result->name)) goto done;
    memcpy(result->name, entry->d_name, result->name_len);
    {
        ZZIP_FILE *file = zzip_file_open(archive, result->name, 0);
        if (!file) goto done;
        zzip_ssize_t n = zzip_file_read(file, result->content, sizeof(result->content));
        zzip_file_close(file);
        if (n < 0 || n != entry->st_size) goto done;
        result->content_len = (size_t)n;
    }
    result->entries = 1;
    while (zzip_readdir(archive)) ++result->entries;
    ok = 1;
done:
    zzip_dir_close(archive);
    return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_zip_result result;
    (void)parsarium_parse_zip(data, size, &result);
    return 0;
}
