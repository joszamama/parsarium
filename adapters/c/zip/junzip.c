#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zlib.h>
#include "junzip.h"

static char entry_name[1024];
static unsigned char *entry_data;
static unsigned int entry_size;
static int seen;
static int parsed;

static int read_entry(FILE *archive, int index, JZFileHeader *central, char *name) {
    if (index != 0 || strlen(name) >= sizeof(entry_name)) return 0;
    seen = 1;
    strcpy(entry_name, name);
    if (fseek(archive, central->offset, SEEK_SET)) return 0;
    JZFileHeader local;
    char local_name[sizeof(entry_name)];
    if (jzReadLocalFileHeader(archive, &local, local_name, sizeof(local_name)) != Z_OK ||
        strcmp(entry_name, local_name) || local.uncompressedSize > 1024 * 1024)
        return 0;
    entry_size = local.uncompressedSize;
    entry_data = (unsigned char *)malloc((size_t)entry_size + 1);
    if (!entry_data) return 0;
    if (jzReadData(archive, &local, entry_data) != Z_OK) return 0;
    entry_data[entry_size] = 0;
    parsed = 1;
    return 0;
}

static void print_json_string(const unsigned char *bytes, size_t size) {
    putchar('"');
    for (size_t i = 0; i < size; ++i) {
        unsigned char ch = bytes[i];
        if (ch == '"' || ch == '\\') { putchar('\\'); putchar(ch); }
        else if (ch == '\n') fputs("\\n", stdout);
        else if (ch == '\r') fputs("\\r", stdout);
        else if (ch == '\t') fputs("\\t", stdout);
        else if (ch < 0x20) printf("\\u%04x", ch);
        else putchar(ch);
    }
    putchar('"');
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *archive = fopen(argv[1], "rb");
    if (!archive) return 3;
    JZEndRecord end;
    int status = jzReadEndRecord(archive, &end);
    if (status == Z_OK) status = jzReadCentralDirectory(archive, &end, read_entry);
    fclose(archive);
    if (status != Z_OK || end.numEntries != 1 || !seen || !parsed) {
        free(entry_data);
        return 4;
    }
    printf("{\"entries\":%u,\"name\":", end.numEntries);
    print_json_string((const unsigned char *)entry_name, strlen(entry_name));
    fputs(",\"content\":", stdout);
    print_json_string(entry_data, entry_size);
    puts("}");
    free(entry_data);
    return 0;
}
