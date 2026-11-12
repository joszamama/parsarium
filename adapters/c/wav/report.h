#ifndef PARSARIUM_C_WAV_REPORT_H
#define PARSARIUM_C_WAV_REPORT_H

#include <stdint.h>
#include <stdio.h>

static void wav_report(unsigned int sample_rate, unsigned int channels,
                       uint64_t frames, const int16_t samples[4]) {
    printf("{\"sample_rate\":%u,\"channels\":%u,\"frames\":%llu,"
           "\"samples\":[%d,%d,%d,%d]}\n",
           sample_rate, channels, (unsigned long long)frames,
           samples[0], samples[1], samples[2], samples[3]);
}

#endif
