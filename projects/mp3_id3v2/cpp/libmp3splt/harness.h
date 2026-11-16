#pragma once
#include <stddef.h>
#include <stdint.h>
typedef struct Result { int split_status; size_t segment_bytes; unsigned char first[4]; } Result;
int parse_data(const uint8_t *data, size_t size, Result *result);
