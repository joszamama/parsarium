#pragma once
#include <stddef.h>
#include <stdint.h>
typedef struct Result { char title[128]; size_t frames; } Result;
int parse_data(const uint8_t *data, size_t size, Result *result);
