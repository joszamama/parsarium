#include "harness.h"
#include <gst/app/gstappsink.h>
#include <gst/gst.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

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
    GstSample *sample = NULL;
    int ok = 0;
    if (!error && pipeline && source && sink) {
        g_object_set(source, "location", path, NULL);
        if (gst_element_set_state(pipeline, GST_STATE_PLAYING) != GST_STATE_CHANGE_FAILURE)
            sample = gst_app_sink_try_pull_sample(GST_APP_SINK(sink), 2 * GST_SECOND);
    }
    if (sample) {
        GstCaps *caps = gst_sample_get_caps(sample);
        const GstStructure *format = caps ? gst_caps_get_structure(caps, 0) : NULL;
        int rate = 0, channels = 0;
        const char *encoding = format ? gst_structure_get_string(format, "format") : NULL;
        GstBuffer *buffer = gst_sample_get_buffer(sample);
        GstMapInfo mapped;
        if (format && gst_structure_get_int(format, "rate", &rate) &&
            gst_structure_get_int(format, "channels", &channels) &&
            encoding && strcmp(encoding, "S16LE") == 0 && channels == 1 && rate > 0 &&
            buffer && gst_buffer_map(buffer, &mapped, GST_MAP_READ)) {
            if (mapped.size >= 8) {
                result->sample_rate = (unsigned)rate;
                result->channels = (unsigned)channels;
                result->frames = mapped.size / 2;
                for (int i = 0; i < 4; i++)
                    result->samples[i] = (int16_t)((uint16_t)mapped.data[2*i] | ((uint16_t)mapped.data[2*i+1] << 8));
                ok = 1;
            }
            gst_buffer_unmap(buffer, &mapped);
        }
        gst_sample_unref(sample);
    }
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
