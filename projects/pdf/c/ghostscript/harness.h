#pragma once
#include <stddef.h>
#include <stdint.h>
typedef struct Result { int pages; } Result;
int parse_data(const uint8_t *data, size_t size, Result *result);
