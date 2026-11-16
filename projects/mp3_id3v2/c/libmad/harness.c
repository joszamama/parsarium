#include "harness.h"
#include <mad.h>
#include <string.h>
#include <stdlib.h>
int parsarium_parse_mp3(const uint8_t *data, size_t size, struct parsarium_mp3_result *result) {
    if (!data || !result || size < 16 || size > (1u << 20) || memcmp(data, "ID3", 3) != 0) return 0;
    size_t offset = 10 + (((size_t)data[6] & 127) << 21) + (((size_t)data[7] & 127) << 14) +
                    (((size_t)data[8] & 127) << 7) + ((size_t)data[9] & 127);
    if (offset >= size) return 0;
    unsigned char *buffer = (unsigned char *)calloc(size + MAD_BUFFER_GUARD, 1);
    if (!buffer) return 0;
    memcpy(buffer, data, size);
    struct mad_stream stream; struct mad_frame frame; struct mad_synth synth;
    mad_stream_init(&stream); mad_frame_init(&frame); mad_synth_init(&synth);
    mad_stream_buffer(&stream, buffer, (unsigned long)(size + MAD_BUFFER_GUARD));
    mad_stream_skip(&stream, (unsigned long)offset);
    int ok = mad_frame_decode(&frame, &stream) == 0 && frame.header.layer == MAD_LAYER_III;
    if (ok) {
        mad_synth_frame(&synth, &frame);
        result->layer = frame.header.layer; result->sample_rate = frame.header.samplerate;
        result->bit_rate = frame.header.bitrate; result->channels = synth.pcm.channels;
        result->decoded_samples = synth.pcm.length;
    }
    mad_synth_finish(&synth); mad_frame_finish(&frame); mad_stream_finish(&stream);
    free(buffer);
    return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_mp3_result result; (void)parsarium_parse_mp3(data, size, &result); return 0;
}
