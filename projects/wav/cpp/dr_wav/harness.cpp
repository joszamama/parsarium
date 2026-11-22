#define DR_WAV_IMPLEMENTATION
#include <dr_wav.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "harness.h"

int parsarium_parse_wav(const uint8_t *data, size_t size,
                        struct parsarium_wav_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    drwav wav;
    if (!drwav_init_memory(&wav, data, size, NULL)) {
        snprintf(result->error, sizeof(result->error), "drwav_init_memory failed");
        return 0;
    }
    result->sample_rate = wav.sampleRate;
    result->channels = wav.channels;
    result->frames = wav.totalPCMFrameCount;
    /* The first four interleaved samples, as s16: enough frames to hold them. */
    if (wav.channels) {
        drwav_uint64 want = (4 + wav.channels - 1) / wav.channels;
        drwav_int16 *buffer = (drwav_int16 *)calloc((size_t)want * wav.channels, sizeof(drwav_int16));
        if (buffer) {
            drwav_uint64 read = drwav_read_pcm_frames_s16(&wav, want, buffer);
            drwav_uint64 count = read * wav.channels;
            result->sample_count = (unsigned)(count < 4 ? count : 4);
            memcpy(result->samples, buffer, result->sample_count * sizeof(drwav_int16));
            free(buffer);
        }
    }
    drwav_uninit(&wav);
    return 1;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_wav_result result;
    (void)parsarium_parse_wav(data, size, &result);
    return 0;
}
