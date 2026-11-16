#pragma once
#include <stddef.h>
#include <stdint.h>
typedef struct Result { unsigned sample_rate, channels; uint64_t frames, samples; int16_t first[4]; } Result;
int parse_data(const uint8_t *data, size_t size, Result *result);
