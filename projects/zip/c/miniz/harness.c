#include "harness.h"
#include <miniz.h>
#include <string.h>

int parsarium_parse_zip(const uint8_t *data, size_t size,
                        struct parsarium_zip_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    mz_zip_archive archive;
    memset(&archive, 0, sizeof(archive));
    if (!mz_zip_reader_init_mem(&archive, data, size, 0)) return 0;
    int ok = 0;
    mz_uint entries = mz_zip_reader_get_num_files(&archive);
    mz_zip_archive_file_stat info;
    if (!entries || !mz_zip_reader_file_stat(&archive, 0, &info)) goto done;
    result->entries = entries;
    result->name_len = strlen(info.m_filename);
    if (!result->name_len || result->name_len >= sizeof(result->name)) goto done;
    memcpy(result->name, info.m_filename, result->name_len);
    size_t extracted_size = 0;
    void *content = mz_zip_reader_extract_to_heap(&archive, 0, &extracted_size, 0);
    if (!content) goto done;
    if (extracted_size <= sizeof(result->content)) {
        memcpy(result->content, content, extracted_size);
        result->content_len = extracted_size;
        ok = 1;
    }
    mz_free(content);
done:
    mz_zip_reader_end(&archive);
    return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_zip_result result;
    (void)parsarium_parse_zip(data, size, &result);
    return 0;
}
