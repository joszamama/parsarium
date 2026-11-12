#include <unarr.h>
#include <string.h>
#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    ar_stream *stream = ar_open_file(argv[1]);
    if (!stream) return 1;
    ar_archive *archive = ar_open_zip_archive(stream, false);
    if (!archive || !ar_parse_entry(archive)) {
        if (archive) ar_close_archive(archive);
        ar_close(stream); return 1;
    }
    const char *entry_name = ar_entry_get_name(archive);
    size_t size = ar_entry_get_size(archive);
    char name[256];
    unsigned char contents[4096];
    if (!entry_name || strlen(entry_name) >= sizeof name || size > sizeof contents ||
        !ar_entry_uncompress(archive, contents, size)) {
        ar_close_archive(archive); ar_close(stream); return 1;
    }
    strcpy(name, entry_name);
    size_t entries = 1;
    while (ar_parse_entry(archive)) entries++;
    if (!ar_at_eof(archive)) { ar_close_archive(archive); ar_close(stream); return 1; }
    zip_report(entries, name, contents, size);
    ar_close_archive(archive);
    ar_close(stream);
    return 0;
}
