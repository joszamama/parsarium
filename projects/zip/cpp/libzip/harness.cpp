#include "harness.hpp"

#include <zip.h>

#include <cstring>

constexpr std::size_t max_input = 1u << 20;

bool parsarium_parse_zip(const std::uint8_t *data, std::size_t size,
                         parsarium_zip_result *result) {
    if (!data || !result || size == 0 || size > max_input) return false;
    *result = {};

    zip_error_t error;
    zip_error_init(&error);
    zip_source_t *source = zip_source_buffer_create(data, size, 0, &error);
    if (!source) {
        zip_error_fini(&error);
        return false;
    }
    zip_t *archive = zip_open_from_source(source, ZIP_RDONLY, &error);
    if (!archive) {
        zip_source_free(source);
        zip_error_fini(&error);
        return false;
    }
    zip_error_fini(&error);

    bool ok = false;
    zip_stat_t stat;
    zip_int64_t count = zip_get_num_entries(archive, 0);
    if (count <= 0) goto done;
    result->entries = count;
    if (zip_stat_index(archive, 0, 0, &stat) < 0 || !stat.name) goto done;
    result->name_len = std::strlen(stat.name);
    if (result->name_len == 0 || result->name_len >= sizeof(result->name) ||
        stat.size > sizeof(result->content)) goto done;
    std::memcpy(result->name, stat.name, result->name_len);
    {
        zip_file_t *entry = zip_fopen_index(archive, 0, 0);
        if (!entry) goto done;
        while (result->content_len < stat.size) {
            zip_int64_t got = zip_fread(entry, result->content + result->content_len,
                                       stat.size - result->content_len);
            if (got <= 0) break;
            result->content_len += static_cast<std::size_t>(got);
        }
        ok = result->content_len == stat.size;
        zip_fclose(entry);
    }
done:
    zip_discard(archive);
    return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    parsarium_zip_result result;
    (void)parsarium_parse_zip(data, size, &result);
    return 0;
}
