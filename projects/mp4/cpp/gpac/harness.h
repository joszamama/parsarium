#ifndef PARSARIUM_GPAC_CPP_MP4_HARNESS_H
#define PARSARIUM_GPAC_CPP_MP4_HARNESS_H
#include <stddef.h>
#include <stdint.h>
/* JSON line printed by the selected C++ call site, adapters/cpp/mp4/gpac.cpp. */
struct parsarium_mp4_result { char json[512]; };
int parsarium_parse_mp4(const uint8_t *data,size_t size,struct parsarium_mp4_result *result);
#endif
