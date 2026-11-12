#include <zipfile/zipfile.h>
#include <stdio.h>
#include <stdlib.h>

#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *input = fopen(argv[1], "rb");
    if (!input || fseek(input, 0, SEEK_END) != 0) return 3;
    long length = ftell(input);
    if (length < 0 || fseek(input, 0, SEEK_SET) != 0) return 4;
    unsigned char *bytes = malloc((size_t)length);
    if (!bytes || fread(bytes, 1, (size_t)length, input) != (size_t)length) return 5;
    fclose(input);
    zipfile_t archive = init_zipfile(bytes, (size_t)length);
    if (!archive) return 6;
    void *cookie = NULL;
    zipentry_t entry;
    zipentry_t first = NULL;
    size_t entries = 0;
    while ((entry = iterate_zipfile(archive, &cookie)) != NULL) {
        if (!first) first = entry;
        entries++;
    }
    if (!first) return 7;
    char *name = get_zipentry_name(first);
    size_t size = get_zipentry_size(first);
    unsigned char *content = malloc(size + 32);
    if (!name || !content || decompress_zipentry(first, content, (int)(size + 32)) != 0) return 8;
    zip_report(entries, name, content, size);
    free(content);
    free(name);
    release_zipfile(archive);
    free(bytes);
    return 0;
}
