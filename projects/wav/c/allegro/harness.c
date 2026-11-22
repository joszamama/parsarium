#include "harness.h"
#include <allegro5/allegro.h>
#include <allegro5/allegro_audio.h>
#include <allegro5/allegro_acodec.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/* One decoded sample as s16, for libraries that hand back their native
   sample format: unsigned integers are re-centred, wider integers keep their
   top 16 bits, floats are scaled by 32768, rounded and clamped. */
static int16_t parsarium_to_s16(const uint8_t *p, char kind, int bytes, int big_endian) {
    uint64_t raw = 0;
    for (int i = 0; i < bytes; i++)
        raw |= (uint64_t)p[big_endian ? i : bytes - 1 - i] << (8 * (bytes - 1 - i));
    if (kind == 'f') {
        double x;
        if (bytes == 4) { uint32_t bits = (uint32_t)raw; float f; memcpy(&f, &bits, 4); x = f; }
        else { double d; memcpy(&d, &raw, 8); x = d; }
        x = x * 32768.0;
        if (!(x > -32768.0)) return x != x ? 0 : -32768;
        if (x >= 32767.0) return 32767;
        return (int16_t)(x >= 0 ? x + 0.5 : x - 0.5); /* half away from zero */
    }
    if (kind == 'u') raw ^= (uint64_t)1 << (8 * bytes - 1);
    uint64_t top = bytes >= 2 ? raw >> (8 * bytes - 16) : raw << 8;
    return (int16_t)(uint16_t)(top & 0xFFFF);
}

/* Allegro reports why a load failed only through its trace log; keep the
   last error line it traces (release logging, level "error"). */
static char trace_line[256];
static void on_trace(const char *line) {
    const char *message = strstr(line, "] ");
    snprintf(trace_line, sizeof(trace_line), "%s", message ? message + 2 : line);
    trace_line[strcspn(trace_line, "\n")] = 0;
}

/* The first samples of an ALLEGRO_SAMPLE in its own depth, as s16. */
static unsigned first_samples(ALLEGRO_SAMPLE *sample, unsigned channels, int16_t out[4]) {
    const uint8_t *pcm = (const uint8_t *)al_get_sample_data(sample);
    ALLEGRO_AUDIO_DEPTH depth = al_get_sample_depth(sample);
    unsigned long long count = (unsigned long long)al_get_sample_length(sample) * channels;
    unsigned n = (unsigned)(count < 4 ? count : 4);
    if (!pcm) return 0;
    for (unsigned i = 0; i < n; i++) {
        switch (depth) {
        case ALLEGRO_AUDIO_DEPTH_INT8: out[i] = parsarium_to_s16(pcm + i, 's', 1, 0); break;
        case ALLEGRO_AUDIO_DEPTH_UINT8: out[i] = parsarium_to_s16(pcm + i, 'u', 1, 0); break;
        case ALLEGRO_AUDIO_DEPTH_INT16: { int16_t v; memcpy(&v, pcm + 2 * i, 2); out[i] = v; break; }
        case ALLEGRO_AUDIO_DEPTH_UINT16: { uint16_t v; memcpy(&v, pcm + 2 * i, 2); out[i] = (int16_t)(v ^ 0x8000u); break; }
        case ALLEGRO_AUDIO_DEPTH_INT24: { int32_t v; memcpy(&v, pcm + 4 * i, 4); out[i] = (int16_t)(v >> 8); break; }
        case ALLEGRO_AUDIO_DEPTH_UINT24: { int32_t v; memcpy(&v, pcm + 4 * i, 4); out[i] = (int16_t)((v - 0x800000) >> 8); break; }
        case ALLEGRO_AUDIO_DEPTH_FLOAT32: out[i] = parsarium_to_s16(pcm + 4 * i, 'f', 4, 0); break;
        default: return i;
        }
    }
    return n;
}

int parse_data(const uint8_t *data, size_t size, Result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.wav";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    int ok = 0;
    setenv("ALLEGRO_TRACE_LEVEL", "error", 0);
    al_register_trace_handler(on_trace);
    if (!al_install_audio() || !al_init_acodec_addon()) {
        snprintf(result->error, sizeof(result->error), "Allegro audio addon initialisation failed");
    } else {
        trace_line[0] = 0;
        ALLEGRO_SAMPLE *sample = al_load_sample(path);
        if (!sample) {
            snprintf(result->error, sizeof(result->error), "al_load_sample failed%s%s",
                     trace_line[0] ? ": " : "", trace_line);
        } else {
            unsigned channels = (unsigned)al_get_channel_count(al_get_sample_channels(sample));
            result->sample_rate = al_get_sample_frequency(sample);
            result->channels = channels;
            result->frames = al_get_sample_length(sample);
            result->sample_count = first_samples(sample, channels, result->samples);
            ok = 1;
            al_destroy_sample(sample);
        }
        al_uninstall_audio();
    }
    unlink(path);
    return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    Result result;
    (void)parse_data(data, size, &result);
    return 0;
}
