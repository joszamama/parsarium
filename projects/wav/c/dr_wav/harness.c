#define DR_WAV_IMPLEMENTATION
#include <dr_wav.h>
#include "harness.h"

int parsarium_parse_wav(const uint8_t *data, size_t size,
                        struct parsarium_wav_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    drwav wav;
    if (!drwav_init_memory(&wav, data, size, NULL)) return 0;
    result->sample_rate = wav.sampleRate;
    result->channels = wav.channels;
    result->frames = wav.totalPCMFrameCount;
    drwav_uint64 read = drwav_read_pcm_frames_s16(&wav, 4, result->samples);
    drwav_uninit(&wav);
    return read == 4;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_wav_result result;
    (void)parsarium_parse_wav(data, size, &result);
    return 0;
}
