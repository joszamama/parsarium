#define MA_NO_DEVICE_IO
#define MA_NO_ENCODING
#define MA_NO_FLAC
#define MINIAUDIO_IMPLEMENTATION
#include <miniaudio.h>
#include "harness.h"

int parsarium_parse_mp3(const uint8_t *data, size_t size,
                        struct parsarium_mp3_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    *result = {};
    ma_decoder decoder;
    ma_decoder_config config = ma_decoder_config_init(ma_format_f32, 0, 0);
    if (ma_decoder_init_memory(data, size, &config, &decoder) != MA_SUCCESS) return 0;
    float sample[2] = {0};
    ma_uint64 decoded = 0, length = 0;
    int ok = decoder.outputChannels <= 2 &&
        ma_decoder_read_pcm_frames(&decoder, sample, 1, &decoded) == MA_SUCCESS &&
        ma_decoder_get_length_in_pcm_frames(&decoder, &length) == MA_SUCCESS &&
        decoded == 1;
    if (ok) {
        result->sample_rate = decoder.outputSampleRate;
        result->channels = decoder.outputChannels;
        result->frames = length;
        result->decoded_frames = decoded;
    }
    ma_decoder_uninit(&decoder);
    return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_mp3_result result;
    (void)parsarium_parse_mp3(data, size, &result);
    return 0;
}
