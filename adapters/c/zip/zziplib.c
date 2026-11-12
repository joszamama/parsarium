#include <zzip/zzip.h>
#include <string.h>
#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    zzip_error_t error = 0;
    ZZIP_DIR *archive = zzip_dir_open(argv[1], &error);
    if (!archive) return 1;
    ZZIP_DIRENT *entry = zzip_readdir(archive);
    char name[256];
    if (!entry || !entry->d_name || strlen(entry->d_name) >= sizeof name ||
        entry->st_size < 0 || entry->st_size > 4096) {
        zzip_dir_close(archive); return 1;
    }
    strcpy(name, entry->d_name);
    ZZIP_FILE *file = zzip_file_open(archive, name, 0);
    if (!file) { zzip_dir_close(archive); return 1; }
    unsigned char contents[4096];
    zzip_ssize_t n = zzip_file_read(file, contents, sizeof contents);
    if (n < 0 || n != entry->st_size || zzip_file_close(file) != 0) {
        zzip_dir_close(archive); return 1;
    }
    size_t entries = 1;
    while (zzip_readdir(archive)) entries++;
    zip_report(entries, name, contents, (size_t) n);
    zzip_dir_close(archive);
    return 0;
}
