#ifndef PARSARIUM_C_ZIP_REPORT_H
#define PARSARIUM_C_ZIP_REPORT_H

#include <stddef.h>
#include <stdio.h>

static void zip_json_string(const unsigned char *bytes, size_t length) {
    putchar('"');
    for (size_t i = 0; i < length; ++i) {
        unsigned c = bytes[i];
        if (c == '"' || c == '\\') { putchar('\\'); putchar((int) c); }
        else if (c >= 32 && c < 127) putchar((int) c);
        else printf("\\u%04x", c);
    }
    putchar('"');
}

static void zip_report(size_t entries, const char *name,
                       const unsigned char *contents, size_t content_length) {
    printf("{\"entries\":%zu,\"name\":", entries);
    size_t name_length = 0;
    while (name[name_length]) name_length++;
    zip_json_string((const unsigned char *) name, name_length);
    printf(",\"content\":");
    zip_json_string(contents, content_length);
    printf("}\n");
}

#endif
