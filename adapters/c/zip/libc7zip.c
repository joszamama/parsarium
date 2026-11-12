#include <libc7zip.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>

#include "report.h"

struct output {
    unsigned char bytes[256];
    size_t length;
};

static int read_local(int64_t id, void *data, int64_t size, int64_t *done) {
    FILE *file = (FILE *)(intptr_t)id;
    *done = (int64_t)fread(data, 1, (size_t)size, file);
    return ferror(file) ? 1 : 0;
}

static int seek_local(int64_t id, int64_t offset, int32_t whence, int64_t *position) {
    FILE *file = (FILE *)(intptr_t)id;
    if (fseeko(file, (off_t)offset, whence) != 0) return 1;
    *position = (int64_t)ftello(file);
    return 0;
}

static int write_output(int64_t id, const void *data, int64_t size, int64_t *done) {
    struct output *out = (struct output *)(intptr_t)id;
    if (size < 0 || (uint64_t)size > sizeof(out->bytes) - out->length) return 1;
    memcpy(out->bytes + out->length, data, (size_t)size);
    out->length += (size_t)size;
    *done = size;
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file || fseeko(file, 0, SEEK_END) != 0) return 3;
    off_t size = ftello(file);
    if (size < 0 || fseeko(file, 0, SEEK_SET) != 0) return 4;

    lib *library = lib_new();
    if (!library) return 5;
    in_stream *input = in_stream_new();
    in_stream_def *input_def = in_stream_get_def(input);
    input_def->id = (int64_t)(intptr_t)file;
    input_def->read_cb = read_local;
    input_def->seek_cb = seek_local;
    input_def->size = (int64_t)size;
    input_def->ext = strdup("zip");
    in_stream_commit_def(input);

    archive *parsed = archive_open(library, input, 1);
    if (!parsed) return 6;
    int64_t entries = archive_get_item_count(parsed);
    if (entries != 1) return 7;
    item *first = archive_get_item(parsed, 0);
    if (!first) return 8;
    int32_t success = 0;
    char *name = item_get_string_property(first, kpidPath, &success);
    if (!success || !name) return 9;
    struct output out = {0};
    out_stream *sink = out_stream_new();
    out_stream_def *sink_def = out_stream_get_def(sink);
    sink_def->id = (int64_t)(intptr_t)&out;
    sink_def->write_cb = write_output;
    if (!archive_extract_item(parsed, first, sink)) return 10;
    zip_report((size_t)entries, name, out.bytes, out.length);

    out_stream_free(sink);
    string_free(name);
    item_free(first);
    archive_close(parsed);
    archive_free(parsed);
    free(input_def->ext);
    in_stream_free(input);
    lib_free(library);
    fclose(file);
    return 0;
}
