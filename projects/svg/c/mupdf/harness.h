#pragma once
#include <stddef.h>
#include <stdint.h>
typedef struct Result { int width, height; uint8_t first[3], second[3]; } Result;
int parse_data(const uint8_t *data, size_t size, Result *result);
