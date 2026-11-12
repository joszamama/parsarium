#include <zip.h>
#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int error = 0;
    zip_t *archive = zip_open(argv[1], ZIP_RDONLY, &error);
    if (!archive) return 1;
    zip_int64_t entries = zip_get_num_entries(archive, 0);
    zip_stat_t entry;
    zip_stat_init(&entry);
    if (entries < 1 || zip_stat_index(archive, 0, 0, &entry) != 0 ||
        !entry.name || entry.size > 4096) { zip_discard(archive); return 1; }
    zip_file_t *file = zip_fopen_index(archive, 0, 0);
    if (!file) { zip_discard(archive); return 1; }
    unsigned char contents[4096];
    zip_int64_t n = zip_fread(file, contents, sizeof contents);
    if (n < 0 || (zip_uint64_t) n != entry.size) {
        zip_fclose(file); zip_discard(archive); return 1;
    }
    zip_report((size_t) entries, entry.name, contents, (size_t) n);
    zip_fclose(file);
    zip_close(archive);
    return 0;
}
