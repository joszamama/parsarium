#define MA_NO_DEVICE_IO
#define MA_NO_ENCODING
#define MA_NO_FLAC
#define MA_NO_MP3
#include <miniaudio.h>
#include <stdint.h>

#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    ma_decoder decoder;
    ma_decoder_config config = ma_decoder_config_init(ma_format_s16, 1, 8000);
    if (ma_decoder_init_file(argv[1], &config, &decoder) != MA_SUCCESS) return 3;
    ma_format format;
    ma_uint32 channels = 0, sample_rate = 0;
    ma_uint64 frames = 0, read = 0;
    int16_t samples[4] = {0};
    if (ma_decoder_get_data_format(&decoder, &format, &channels, &sample_rate, NULL, 0) != MA_SUCCESS ||
        ma_decoder_get_length_in_pcm_frames(&decoder, &frames) != MA_SUCCESS ||
        ma_decoder_read_pcm_frames(&decoder, samples, 4, &read) != MA_SUCCESS ||
        format != ma_format_s16 || read != 4) {
        ma_decoder_uninit(&decoder);
        return 4;
    }
    wav_report(sample_rate, channels, frames, samples);
    ma_decoder_uninit(&decoder);
    return 0;
}
