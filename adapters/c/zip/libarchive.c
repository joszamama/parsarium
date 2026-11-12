#include <archive.h>
#include <archive_entry.h>
#include <string.h>
#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    struct archive *archive = archive_read_new();
    if (!archive) return 1;
    if (archive_read_support_format_zip(archive) != ARCHIVE_OK ||
        archive_read_open_filename(archive, argv[1], 10240) != ARCHIVE_OK) {
        archive_read_free(archive); return 1;
    }
    struct archive_entry *entry;
    char name[256] = {0};
    unsigned char contents[4096];
    size_t content_length = 0, entries = 0;
    int status;
    while ((status = archive_read_next_header(archive, &entry)) == ARCHIVE_OK) {
        entries++;
        if (entries == 1) {
            const char *path = archive_entry_pathname(entry);
            if (!path || strlen(path) >= sizeof name) { archive_read_free(archive); return 1; }
            strcpy(name, path);
            la_ssize_t read_count;
            while ((read_count = archive_read_data(archive, contents + content_length,
                                                  sizeof contents - content_length)) > 0) {
                content_length += (size_t) read_count;
                if (content_length == sizeof contents) break;
            }
            if (read_count < 0) { archive_read_free(archive); return 1; }
        }
    }
    if (status != ARCHIVE_EOF || entries == 0) { archive_read_free(archive); return 1; }
    zip_report(entries, name, contents, content_length);
    archive_read_free(archive);
    return 0;
}
