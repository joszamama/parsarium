#include "harness.h"
#include <gst/app/gstappsink.h>
#include <gst/gst.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
int parsarium_parse_pnm(const uint8_t *data, size_t size, struct parsarium_pnm_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.ppm";
    int fd = mkstemps(path, 4); if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    gst_init(NULL, NULL);
    GError *error = NULL;
    GstElement *pipeline = gst_parse_launch("filesrc name=source ! pnmdec ! appsink name=sink sync=false", &error);
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
        int width = 0, height = 0;
        const char *encoding = format ? gst_structure_get_string(format, "format") : NULL;
        GstBuffer *buffer = gst_sample_get_buffer(sample);
        GstMapInfo mapped;
        if (format && gst_structure_get_int(format, "width", &width) &&
            gst_structure_get_int(format, "height", &height) &&
            encoding && strcmp(encoding, "RGB") == 0 && width > 0 && height > 0 &&
            buffer && gst_buffer_map(buffer, &mapped, GST_MAP_READ)) {
            /* Raw RGB rows are padded to four bytes; the second pixel is the
               next one in raster order, if the image has one. */
            size_t stride = GST_ROUND_UP_4((size_t)width * 3);
            size_t second = width > 1 ? 3 : height > 1 ? stride : 0;
            if (mapped.size >= 3 && mapped.size >= second + 3) {
                result->width = (unsigned)width;
                result->height = (unsigned)height;
                memcpy(result->format, "RGB", 4);
                memcpy(result->first, mapped.data, 3);
                result->has_second = second != 0;
                if (second) memcpy(result->second, mapped.data + second, 3);
                ok = 1;
            }
            gst_buffer_unmap(buffer, &mapped);
        }
        gst_sample_unref(sample);
    }
    if (!ok && pipeline) {
        /* Report the errors GStreamer posted, verbatim, instead of a bare failure. */
        GstBus *bus = gst_element_get_bus(pipeline);
        GstMessage *message;
        int reported = 0;
        while (bus && (message = gst_bus_pop_filtered(bus, GST_MESSAGE_ERROR))) {
            GError *posted = NULL;
            gchar *debug = NULL;
            gst_message_parse_error(message, &posted, &debug);
            if (debug) g_strdelimit(debug, "\n", ' ');
            fprintf(stderr, "GStreamer error from %s: %s (%s)\n",
                    GST_MESSAGE_SRC_NAME(message), posted ? posted->message : "unknown",
                    debug ? debug : "no debug info");
            if (posted) g_error_free(posted);
            g_free(debug);
            gst_message_unref(message);
            reported = 1;
        }
        if (bus) gst_object_unref(bus);
        if (!reported)
            fprintf(stderr, "GStreamer posted no error; %s\n",
                    sample ? "the decoded sample was not an RGB frame" : "no decoded sample");
    }
    if (pipeline) { gst_element_set_state(pipeline, GST_STATE_NULL); gst_object_unref(pipeline); }
    if (source) gst_object_unref(source);
    if (sink) gst_object_unref(sink);
    if (error) g_error_free(error);
    unlink(path);
    return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_pnm_result result;
    (void)parsarium_parse_pnm(data, size, &result);
    return 0;
}
