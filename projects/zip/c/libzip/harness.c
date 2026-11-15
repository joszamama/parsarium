#include "harness.h"

#include <zip.h>
#include <string.h>

#define PARSARIUM_MAX_INPUT (1u << 20)

int parsarium_parse_zip(const uint8_t *data, size_t size,
                        struct parsarium_zip_result *result) {
    if (!data || !result || size == 0 || size > PARSARIUM_MAX_INPUT) return 0;
    memset(result, 0, sizeof(*result));

    zip_error_t error;
    zip_error_init(&error);
    zip_source_t *source = zip_source_buffer_create(data, size, 0, &error);
    if (!source) {
        zip_error_fini(&error);
        return 0;
    }
    zip_t *archive = zip_open_from_source(source, ZIP_RDONLY, &error);
    if (!archive) {
        zip_source_free(source);
        zip_error_fini(&error);
        return 0;
    }
    zip_error_fini(&error);

    int ok = 0;
    zip_int64_t count = zip_get_num_entries(archive, 0);
    if (count <= 0) goto done;
    result->entries = count;
    zip_stat_t stat;
    if (zip_stat_index(archive, 0, 0, &stat) < 0 || !stat.name) goto done;
    result->name_len = strlen(stat.name);
    if (result->name_len == 0 || result->name_len >= sizeof(result->name) ||
        stat.size > sizeof(result->content)) goto done;
    memcpy(result->name, stat.name, result->name_len);
    zip_file_t *entry = zip_fopen_index(archive, 0, 0);
    if (!entry) goto done;
    while (result->content_len < stat.size) {
        zip_int64_t got = zip_fread(entry, result->content + result->content_len,
                                   stat.size - result->content_len);
        if (got <= 0) break;
        result->content_len += (size_t)got;
    }
    ok = result->content_len == stat.size;
    zip_fclose(entry);

done:
    zip_discard(archive);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_zip_result result;
    (void)parsarium_parse_zip(data, size, &result);
    return 0;
}
