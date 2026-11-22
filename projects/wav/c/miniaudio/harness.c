#define MA_NO_DEVICE_IO
#define MA_NO_ENCODING
#define MA_NO_FLAC
#define MA_NO_MP3
#define MINIAUDIO_IMPLEMENTATION
#include <miniaudio.h>
#include <stdio.h>
#include <string.h>
#include "harness.h"

static int failed(struct parsarium_wav_result *result, const char *call, ma_result code) {
    snprintf(result->error, sizeof(result->error), "%s: %s", call, ma_result_description(code));
    return 0;
}

int parsarium_parse_wav(const uint8_t *data, size_t size,
                        struct parsarium_wav_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    ma_decoder decoder;
    /* s16 output in the file's own channel count and sample rate. */
    ma_decoder_config config = ma_decoder_config_init(ma_format_s16, 0, 0);
    ma_result code = ma_decoder_init_memory(data, size, &config, &decoder);
    if (code != MA_SUCCESS) return failed(result, "ma_decoder_init_memory", code);
    ma_format format;
    ma_uint32 channels = 0, sample_rate = 0;
    ma_uint64 frames = 0, read = 0;
    int ok = 0;
    if ((code = ma_decoder_get_data_format(&decoder, &format, &channels, &sample_rate, NULL, 0)) != MA_SUCCESS)
        failed(result, "ma_decoder_get_data_format", code);
    else if ((code = ma_decoder_get_length_in_pcm_frames(&decoder, &frames)) != MA_SUCCESS)
        failed(result, "ma_decoder_get_length_in_pcm_frames", code);
    else if (channels) {
        /* The first four interleaved samples: enough frames to hold them. */
        ma_int16 buffer[4 * MA_MAX_CHANNELS];
        ma_uint64 want = (4 + channels - 1) / channels;
        code = ma_decoder_read_pcm_frames(&decoder, buffer, want, &read);
        if (code != MA_SUCCESS && code != MA_AT_END) {
            failed(result, "ma_decoder_read_pcm_frames", code);
        } else {
            ma_uint64 count = read * channels;
            result->sample_rate = sample_rate;
            result->channels = channels;
            result->frames = frames;
            result->sample_count = (unsigned)(count < 4 ? count : 4);
            memcpy(result->samples, buffer, result->sample_count * sizeof(ma_int16));
            ok = 1;
        }
    } else {
        result->sample_rate = sample_rate;
        result->frames = frames;
        ok = 1;
    }
    ma_decoder_uninit(&decoder);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_wav_result result;
    (void)parsarium_parse_wav(data, size, &result);
    return 0;
}
