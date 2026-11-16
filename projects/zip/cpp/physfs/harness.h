#ifndef PARSARIUM_MINIZIP_HARNESS_H
#define PARSARIUM_MINIZIP_HARNESS_H

#include <stddef.h>
#include <stdint.h>

struct parsarium_zip_result {
    int64_t entries;
    char name[256];
    size_t name_len;
    unsigned char content[4096];
    size_t content_len;
};

int parsarium_parse_zip(const uint8_t *data, size_t size,
                        struct parsarium_zip_result *result);

#endif
