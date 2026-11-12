#include <minizip/unzip.h>
#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    unzFile archive = unzOpen64(argv[1]);
    if (!archive) return 1;
    unz_global_info64 global;
    unz_file_info64 info;
    char name[256] = {0};
    if (unzGetGlobalInfo64(archive, &global) != UNZ_OK || global.number_entry < 1 ||
        unzGoToFirstFile(archive) != UNZ_OK ||
        unzGetCurrentFileInfo64(archive, &info, name, sizeof name, NULL, 0, NULL, 0) != UNZ_OK ||
        unzOpenCurrentFile(archive) != UNZ_OK) { unzClose(archive); return 1; }
    unsigned char contents[4096];
    int n = unzReadCurrentFile(archive, contents, sizeof contents);
    if (n < 0 || (unsigned long long) n != info.uncompressed_size ||
        unzCloseCurrentFile(archive) != UNZ_OK) { unzClose(archive); return 1; }
    zip_report((size_t) global.number_entry, name, contents, (size_t) n);
    unzClose(archive);
    return 0;
}
