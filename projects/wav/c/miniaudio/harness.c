#define MA_NO_DEVICE_IO
#define MA_NO_ENCODING
#define MA_NO_FLAC
#define MA_NO_MP3
#define MINIAUDIO_IMPLEMENTATION
#include <miniaudio.h>
#include "harness.h"

int parsarium_parse_wav(const uint8_t *data, size_t size,
                        struct parsarium_wav_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    *result = (struct parsarium_wav_result){0};
    ma_decoder decoder;
    ma_decoder_config config = ma_decoder_config_init(ma_format_s16, 1, 8000);
    if (ma_decoder_init_memory(data, size, &config, &decoder) != MA_SUCCESS) return 0;
    ma_format format;
    ma_uint32 channels = 0, sample_rate = 0;
    ma_uint64 frames = 0, read = 0;
    int ok = ma_decoder_get_data_format(&decoder, &format, &channels, &sample_rate, NULL, 0) == MA_SUCCESS &&
        ma_decoder_get_length_in_pcm_frames(&decoder, &frames) == MA_SUCCESS &&
        ma_decoder_read_pcm_frames(&decoder, result->samples, 4, &read) == MA_SUCCESS &&
        format == ma_format_s16 && read == 4;
    if (ok) {
        result->sample_rate = sample_rate;
        result->channels = channels;
        result->frames = frames;
    }
    ma_decoder_uninit(&decoder);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_wav_result result;
    (void)parsarium_parse_wav(data, size, &result);
    return 0;
}
