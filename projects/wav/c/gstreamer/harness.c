#include "harness.h"
#include <gst/app/gstappsink.h>
#include <gst/gst.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
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

/* Sample layout of a GstAudioFormat name such as S16LE, U8, S24LE or F32LE. */
static int sample_layout(const char *name, char *kind, int *bytes, int *big_endian) {
    if (!name || (name[0] != 'S' && name[0] != 'U' && name[0] != 'F')) return 0;
    char *end = NULL;
    long bits = strtol(name + 1, &end, 10);
    if (bits <= 0 || bits % 8 || bits > 64) return 0;
    if (*end == '_') return 0; /* padded layouts such as S24_32LE */
    if (*end && strcmp(end, "LE") != 0 && strcmp(end, "BE") != 0) return 0;
    *kind = name[0] == 'F' ? 'f' : name[0] == 'U' ? 'u' : 's';
    *bytes = (int)(bits / 8);
    *big_endian = strcmp(end, "BE") == 0;
    return 1;
}

int parsarium_parse_wav(const uint8_t *data, size_t size, struct parsarium_wav_result *result) {
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
    gst_init(NULL, NULL);
    GError *error = NULL;
    GstElement *pipeline = gst_parse_launch("filesrc name=source ! wavparse ! appsink name=sink sync=false", &error);
    GstElement *source = pipeline ? gst_bin_get_by_name(GST_BIN(pipeline), "source") : NULL;
    GstElement *sink = pipeline ? gst_bin_get_by_name(GST_BIN(pipeline), "sink") : NULL;
    int ok = 0, started = 0;
    if (!error && pipeline && source && sink) {
        g_object_set(source, "location", path, NULL);
        started = gst_element_set_state(pipeline, GST_STATE_PLAYING) != GST_STATE_CHANGE_FAILURE;
    }
    /* Pull every buffer wavparse emits: the first caps give the format, the
       first buffers the first four samples, and the byte total the frames. */
    unsigned long long total = 0;
    int bytes = 0, frame_bytes = 0, big_endian = 0, have_caps = 0;
    char kind = 's';
    GstSample *sample;
    while (started && (sample = gst_app_sink_try_pull_sample(GST_APP_SINK(sink), 2 * GST_SECOND))) {
        GstBuffer *buffer = gst_sample_get_buffer(sample);
        if (!have_caps) {
            GstCaps *caps = gst_sample_get_caps(sample);
            const GstStructure *format = caps ? gst_caps_get_structure(caps, 0) : NULL;
            int rate = 0, channels = 0;
            const char *encoding = format ? gst_structure_get_string(format, "format") : NULL;
            if (format && gst_structure_get_int(format, "rate", &rate) &&
                gst_structure_get_int(format, "channels", &channels) && channels > 0 &&
                sample_layout(encoding, &kind, &bytes, &big_endian)) {
                result->sample_rate = (unsigned)rate;
                result->channels = (unsigned)channels;
                frame_bytes = bytes * channels;
                have_caps = 1;
            } else {
                gchar *text = caps ? gst_caps_to_string(caps) : NULL;
                snprintf(result->error, sizeof(result->error), "unhandled wavparse caps: %s", text ? text : "none");
                g_free(text);
                gst_sample_unref(sample);
                break;
            }
        }
        GstMapInfo mapped;
        if (buffer && gst_buffer_map(buffer, &mapped, GST_MAP_READ)) {
            for (size_t at = 0; result->sample_count < 4 && at + (size_t)bytes <= mapped.size; at += (size_t)bytes)
                result->samples[result->sample_count++] = parsarium_to_s16(mapped.data + at, kind, bytes, big_endian);
            total += mapped.size;
            gst_buffer_unmap(buffer, &mapped);
        }
        gst_sample_unref(sample);
    }
    /* An error posted on the bus is the library's answer, even after buffers. */
    GstBus *bus = pipeline ? gst_element_get_bus(pipeline) : NULL;
    GstMessage *message = bus ? gst_bus_pop_filtered(bus, GST_MESSAGE_ERROR) : NULL;
    if (message) {
        GError *failure = NULL;
        gst_message_parse_error(message, &failure, NULL);
        snprintf(result->error, sizeof(result->error), "%s", failure ? failure->message : "pipeline error");
        if (failure) g_error_free(failure);
        gst_message_unref(message);
    } else if (have_caps) {
        result->frames = total / (unsigned long long)frame_bytes;
        ok = 1;
    } else if (!result->error[0]) {
        snprintf(result->error, sizeof(result->error), "wavparse produced no samples");
    }
    if (bus) gst_object_unref(bus);
    if (pipeline) { gst_element_set_state(pipeline, GST_STATE_NULL); gst_object_unref(pipeline); }
    if (source) gst_object_unref(source);
    if (sink) gst_object_unref(sink);
    if (error) g_error_free(error);
    unlink(path);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_wav_result result;
    (void)parsarium_parse_wav(data, size, &result);
    return 0;
}
