#include "harness.h"
#include <lame.h>
#include <string.h>
int parsarium_parse_mp3(const uint8_t *data, size_t size, struct parsarium_mp3_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    hip_t decoder = hip_decode_init();
    if (!decoder) return 0;
    short left[1152], right[1152];
    mp3data_struct frame; memset(&frame, 0, sizeof(frame));
    int decoded = hip_decode1_headers(decoder, data, size, left, right, &frame);
    int ok = decoded > 0 && frame.header_parsed;
    if (ok) {
        result->sample_rate = frame.samplerate; result->channels = frame.stereo;
        result->bitrate_kbps = frame.bitrate; result->decoded_samples = (unsigned)decoded;
    }
    hip_decode_exit(decoder);
    return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_mp3_result result; (void)parsarium_parse_mp3(data, size, &result); return 0;
}
