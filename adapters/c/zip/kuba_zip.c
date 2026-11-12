#include <zip.h>
#include <stdlib.h>
#include <string.h>
#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    struct zip_t *archive = zip_open(argv[1], 0, 'r');
    if (!archive) return 1;
    ssize_t entries = zip_entries_total(archive);
    if (entries < 1 || zip_entry_openbyindex(archive, 0) != 0) {
        zip_close(archive); return 1;
    }
    const char *entry_name = zip_entry_name(archive);
    char name[256];
    if (!entry_name || strlen(entry_name) >= sizeof name) {
        zip_entry_close(archive); zip_close(archive); return 1;
    }
    strcpy(name, entry_name);
    void *contents = NULL;
    size_t size = 0;
    ssize_t n = zip_entry_read(archive, &contents, &size);
    if (n < 0 || !contents || (size_t) n != size || zip_entry_close(archive) != 0) {
        free(contents); zip_close(archive); return 1;
    }
    zip_report((size_t) entries, name, (const unsigned char *) contents, size);
    free(contents);
    zip_close(archive);
    return 0;
}
