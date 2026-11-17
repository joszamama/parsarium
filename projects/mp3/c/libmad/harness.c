#include "harness.h"
#include <mad.h>
#include <stdlib.h>
#include <string.h>
/* Decode every MPEG audio frame of a local byte buffer with mad_stream_buffer,
   mad_frame_decode and mad_synth_frame. libmad only decodes a frame when
   MAD_BUFFER_GUARD (8) bytes follow it (src/frame.c), so the input is copied
   into a private buffer with exactly that many zero bytes appended. The zero
   guard then produces one MAD_ERROR_LOSTSYNC at offset `size`; only that error
   is treated as the end of input. Every other recoverable error is counted. */
int parsarium_parse_mp3(const uint8_t *data, size_t size, struct parsarium_mp3_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    unsigned char *buffer = calloc(size + MAD_BUFFER_GUARD, 1);
    if (!buffer) return 0;
    memcpy(buffer, data, size);
    struct mad_stream stream;
    struct mad_frame frame;
    struct mad_synth synth;
    mad_stream_init(&stream);
    mad_frame_init(&frame);
    mad_synth_init(&synth);
    mad_stream_buffer(&stream, buffer, size + MAD_BUFFER_GUARD);
    int ok = 1;
    for (;;) {
        if (mad_frame_decode(&frame, &stream) == -1) {
            if (stream.error == MAD_ERROR_BUFLEN) break;
            if (stream.error == MAD_ERROR_LOSTSYNC && stream.this_frame == buffer + size) {
                result->consumed_bytes = (unsigned long)size;
                continue;
            }
            if (MAD_RECOVERABLE(stream.error)) { result->recoverable_errors++; continue; }
            ok = 0;
            break;
        }
        mad_synth_frame(&synth, &frame);
        const struct mad_header *h = &frame.header;
        if (result->frames && ((unsigned)h->layer != result->layer || h->samplerate != result->sample_rate
                               || synth.pcm.channels != result->channels)) { ok = 0; break; }
        if (!result->frames || h->bitrate < result->bit_rate_min) result->bit_rate_min = h->bitrate;
        if (h->bitrate > result->bit_rate_max) result->bit_rate_max = h->bitrate;
        result->layer = (unsigned)h->layer;
        result->sample_rate = h->samplerate;
        result->channels = synth.pcm.channels;
        result->frames++;
        result->decoded_samples += synth.pcm.length;
    }
    if (!result->consumed_bytes && stream.next_frame) result->consumed_bytes = (unsigned long)(stream.next_frame - buffer);
    ok = ok && result->frames > 0 && result->sample_rate > 0 && result->channels > 0;
    mad_synth_finish(&synth);
    mad_frame_finish(&frame);
    mad_stream_finish(&stream);
    free(buffer);
    return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_mp3_result result; (void)parsarium_parse_mp3(data, size, &result); return 0;
}
