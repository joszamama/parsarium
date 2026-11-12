#include <mz.h>
#include <mz_strm.h>
#include <mz_zip.h>
#include <mz_zip_rw.h>
#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    void *archive = mz_zip_reader_create();
    if (!archive) return 1;
    if (mz_zip_reader_open_file(archive, argv[1]) != MZ_OK ||
        mz_zip_reader_goto_first_entry(archive) != MZ_OK) {
        mz_zip_reader_delete(&archive); return 1;
    }
    mz_zip_file *info = NULL;
    if (mz_zip_reader_entry_get_info(archive, &info) != MZ_OK || !info ||
        !info->filename || info->uncompressed_size > 4096 ||
        mz_zip_reader_entry_open(archive) != MZ_OK) {
        mz_zip_reader_delete(&archive); return 1;
    }
    char name[256] = {0};
    size_t i = 0;
    while (info->filename[i] && i + 1 < sizeof name) { name[i] = info->filename[i]; i++; }
    unsigned char contents[4096];
    int32_t n = mz_zip_reader_entry_read(archive, contents, sizeof contents);
    if (n < 0 || n != info->uncompressed_size ||
        mz_zip_reader_entry_close(archive) != MZ_OK) {
        mz_zip_reader_delete(&archive); return 1;
    }
    size_t entries = 1;
    while (mz_zip_reader_goto_next_entry(archive) == MZ_OK) entries++;
    zip_report(entries, name, contents, (size_t) n);
    mz_zip_reader_close(archive);
    mz_zip_reader_delete(&archive);
    return 0;
}
