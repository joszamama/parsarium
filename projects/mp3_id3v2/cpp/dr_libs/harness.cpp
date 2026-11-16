#define DR_MP3_IMPLEMENTATION
#include <dr_mp3.h>
#include "harness.h"

static void on_meta(void *context, const drmp3_metadata *metadata) {
    struct parsarium_mp3_result *result = static_cast<struct parsarium_mp3_result *>(context);
    if (metadata->type == DRMP3_METADATA_TYPE_ID3V2) {
        result->id3v2_bytes = metadata->rawDataSize;
    }
}

int parsarium_parse_mp3(const uint8_t *data, size_t size,
                        struct parsarium_mp3_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    *result = {};
    drmp3 mp3;
    if (!drmp3_init_memory_with_metadata(&mp3, data, size, on_meta, result, NULL)) return 0;
    drmp3_int16 samples[2] = {0};
    drmp3_uint64 frames = drmp3_read_pcm_frames_s16(&mp3, 1, samples);
    result->sample_rate = mp3.sampleRate;
    result->channels = mp3.channels;
    result->decoded_frames = frames;
    drmp3_uninit(&mp3);
    return frames == 1 && result->id3v2_bytes != 0;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_mp3_result result;
    (void)parsarium_parse_mp3(data, size, &result);
    return 0;
}
