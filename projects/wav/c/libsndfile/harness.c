#include "harness.h"
#include <math.h>
#include <sndfile.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
struct memfile { const uint8_t *data; sf_count_t size, pos; };
static sf_count_t length(void *p) { return ((struct memfile *)p)->size; }
static sf_count_t tell(void *p) { return ((struct memfile *)p)->pos; }
static sf_count_t seek(sf_count_t offset, int whence, void *p) {
    struct memfile *m = p; sf_count_t next = (whence == SEEK_SET ? 0 : whence == SEEK_CUR ? m->pos : m->size) + offset;
    if (next < 0 || next > m->size) return -1; m->pos = next; return next;
}
static sf_count_t readbytes(void *dst, sf_count_t count, void *p) {
    struct memfile *m = p; if (count < 0) return 0;
    if (count > m->size - m->pos) count = m->size - m->pos;
    memcpy(dst, m->data + m->pos, (size_t)count); m->pos += count; return count;
}
static sf_count_t writebytes(const void *src, sf_count_t count, void *p) { (void)src;(void)count;(void)p;return 0; }
int parsarium_parse_wav(const uint8_t *data, size_t size, struct parsarium_wav_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    struct memfile input = {data, (sf_count_t)size, 0};
    SF_VIRTUAL_IO io = {length, seek, readbytes, writebytes, tell};
    SF_INFO info = {0};
    SNDFILE *file = sf_open_virtual(&io, SFM_READ, &info, &input);
    if (!file) {
        snprintf(result->error, sizeof(result->error), "%s", sf_strerror(NULL));
        return 0;
    }
    result->sample_rate = (unsigned)info.samplerate;
    result->channels = (unsigned)info.channels;
    result->frames = (unsigned long long)info.frames;
    /* The first four interleaved samples, as s16: enough frames to hold them. */
    if (info.channels > 0) {
        sf_count_t want = (4 + info.channels - 1) / info.channels;
        int subtype = info.format & SF_FORMAT_SUBMASK;
        if (subtype == SF_FORMAT_FLOAT || subtype == SF_FORMAT_DOUBLE) {
            /* sf_readf_short does not scale float data by default, so every
               sample in [-1, 1] would read as 0. Read the floats and scale
               them to s16 (x 32768, rounded, saturated). */
            float *buffer = (float *)calloc((size_t)(want * info.channels), sizeof(float));
            if (buffer) {
                sf_count_t read = sf_readf_float(file, buffer, want);
                sf_count_t count = read > 0 ? read * info.channels : 0;
                result->sample_count = (unsigned)(count < 4 ? count : 4);
                for (unsigned i = 0; i < result->sample_count; i++) {
                    double scaled = nearbyint((double)buffer[i] * 32768.0);
                    result->samples[i] = (int16_t)(scaled > 32767.0 ? 32767 : scaled < -32768.0 ? -32768 : scaled);
                }
                free(buffer);
            }
        } else {
            short *buffer = (short *)calloc((size_t)(want * info.channels), sizeof(short));
            if (buffer) {
                sf_count_t read = sf_readf_short(file, buffer, want);
                sf_count_t count = read > 0 ? read * info.channels : 0;
                result->sample_count = (unsigned)(count < 4 ? count : 4);
                memcpy(result->samples, buffer, result->sample_count * sizeof(short));
                free(buffer);
            }
        }
    }
    sf_close(file); return 1;
}
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_wav_result result; (void)parsarium_parse_wav(data,size,&result); return 0;
}
