#include <miniz.h>
#include <string.h>
#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    mz_zip_archive archive;
    memset(&archive, 0, sizeof archive);
    if (!mz_zip_reader_init_file(&archive, argv[1], 0)) return 1;
    mz_uint entries = mz_zip_reader_get_num_files(&archive);
    mz_zip_archive_file_stat info;
    if (!entries || !mz_zip_reader_file_stat(&archive, 0, &info)) {
        mz_zip_reader_end(&archive); return 1;
    }
    size_t size = 0;
    void *contents = mz_zip_reader_extract_to_heap(&archive, 0, &size, 0);
    if (!contents) { mz_zip_reader_end(&archive); return 1; }
    zip_report(entries, info.m_filename, contents, size);
    mz_free(contents);
    mz_zip_reader_end(&archive);
    return 0;
}
