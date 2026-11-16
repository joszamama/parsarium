#include "harness.h"
#include <sndfile.h>
#include <stdio.h>
#include <string.h>
struct memfile { const uint8_t *data; sf_count_t size, pos; };
static sf_count_t length(void *p) { return ((struct memfile *)p)->size; }
static sf_count_t tell(void *p) { return ((struct memfile *)p)->pos; }
static sf_count_t seek(sf_count_t offset, int whence, void *p) {
    struct memfile *m = (struct memfile *)p; sf_count_t next = (whence == SEEK_SET ? 0 : whence == SEEK_CUR ? m->pos : m->size) + offset;
    if (next < 0 || next > m->size) return -1; m->pos = next; return next;
}
static sf_count_t readbytes(void *dst, sf_count_t count, void *p) {
    struct memfile *m = (struct memfile *)p; if (count < 0) return 0;
    if (count > m->size - m->pos) count = m->size - m->pos;
    memcpy(dst, m->data + m->pos, (size_t)count); m->pos += count; return count;
}
static sf_count_t writebytes(const void *src, sf_count_t count, void *p) { (void)src;(void)count;(void)p;return 0; }
int parsarium_parse_wav(const uint8_t *data, size_t size, struct parsarium_wav_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    struct memfile input = {data, (sf_count_t)size, 0};
    SF_VIRTUAL_IO io = {length, seek, readbytes, writebytes, tell};
    SF_INFO info = {0};
    SNDFILE *file = sf_open_virtual(&io, SFM_READ, &info, &input);
    if (!file) return 0;
    int ok = (info.format & SF_FORMAT_TYPEMASK) == SF_FORMAT_WAV &&
             info.channels == 1 && info.samplerate == 8000 && info.frames == 4;
    int16_t samples[4] = {0};
    if (ok) ok = sf_readf_short(file, samples, 4) == 4;
    if (ok) { result->sample_rate=info.samplerate; result->channels=info.channels;
              result->frames=info.frames; memcpy(result->samples,samples,sizeof(samples)); }
    sf_close(file); return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_wav_result result; (void)parsarium_parse_wav(data,size,&result); return 0;
}
