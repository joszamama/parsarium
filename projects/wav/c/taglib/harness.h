#pragma once
#include <stddef.h>
#include <stdint.h>
typedef struct Result { int sample_rate, channels, bitrate_kbps; } Result;
int parse_data(const uint8_t *data, size_t size, Result *result);
