#ifndef PARSARIUM_HTTP_CONTROL_H
#define PARSARIUM_HTTP_CONTROL_H

#include <stdio.h>
#include <stdlib.h>

static size_t read_control(const char *path, char *buffer, size_t capacity) {
    FILE *file = fopen(path, "rb");
    if (file == NULL) { perror(path); exit(1); }
    size_t size = fread(buffer, 1, capacity, file);
    if (ferror(file) || !feof(file)) { fprintf(stderr, "control read failed\n"); exit(1); }
    fclose(file);
    return size;
}

#endif
