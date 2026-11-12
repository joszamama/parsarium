#include <unzip.h>
#include "report.h"
#include <limits.h>
#include <stdint.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file || fseek(file, 0, SEEK_END) != 0) return 1;
    const long length = ftell(file);
    if (length < 0 || (unsigned long) length > UINT32_MAX || fseek(file, 0, SEEK_SET) != 0) return 1;
    uint8_t *bytes = (uint8_t *) malloc((size_t) length + 1);
    if (!bytes || fread(bytes, 1, (size_t) length, file) != (size_t) length) return 1;
    fclose(file);

    ZIPFILE state = {0};
    unzFile archive = unzOpen(NULL, bytes, (uint32_t) length, &state,
                              NULL, NULL, NULL, NULL);
    if (!archive) return 1;
    unz_global_info global = {0};
    if (unzGetGlobalInfo(archive, &global) != UNZ_OK || global.number_entry == 0) return 1;
    if (unzGoToFirstFile(archive) != UNZ_OK) return 1;
    unz_file_info info = {0};
    char name[256] = {0};
    if (unzGetCurrentFileInfo(archive, &info, name, sizeof(name),
                              NULL, 0, NULL, 0) != UNZ_OK) return 1;
    if (info.uncompressed_size > SIZE_MAX - 1) return 1;
    unsigned char *content = (unsigned char *) malloc((size_t) info.uncompressed_size + 1);
    if (!content || unzOpenCurrentFile(archive) != UNZ_OK) return 1;
    size_t filled = 0;
    while (filled < (size_t) info.uncompressed_size) {
        const int got = unzReadCurrentFile(archive, content + filled,
                                           (unsigned int) ((size_t) info.uncompressed_size - filled));
        if (got <= 0) return 1;
        filled += (size_t) got;
    }
    if (unzCloseCurrentFile(archive) != UNZ_OK) return 1;
    zip_report(global.number_entry, name, content, filled);
    unzClose(archive);
    free(content);
    free(bytes);
    return 0;
}
