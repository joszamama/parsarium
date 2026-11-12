#include <gst/app/gstappsink.h>
#include <gst/gst.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    gst_init(&argc, &argv);
    GError *error = NULL;
    GstElement *pipeline = gst_parse_launch(
        "filesrc name=source ! wavparse ! appsink name=sink sync=false", &error);
    if (!pipeline || error) return 3;
    GstElement *source = gst_bin_get_by_name(GST_BIN(pipeline), "source");
    GstElement *sink = gst_bin_get_by_name(GST_BIN(pipeline), "sink");
    if (!source || !sink) return 4;
    g_object_set(source, "location", argv[1], NULL);
    if (gst_element_set_state(pipeline, GST_STATE_PLAYING) == GST_STATE_CHANGE_FAILURE) return 5;
    GstSample *sample = gst_app_sink_try_pull_sample(GST_APP_SINK(sink), 5 * GST_SECOND);
    if (!sample) return 6;
    GstCaps *caps = gst_sample_get_caps(sample);
    const GstStructure *format = caps ? gst_caps_get_structure(caps, 0) : NULL;
    int rate = 0, channels = 0;
    const char *encoding = format ? gst_structure_get_string(format, "format") : NULL;
    if (!format || !gst_structure_get_int(format, "rate", &rate) ||
        !gst_structure_get_int(format, "channels", &channels) ||
        !encoding || strcmp(encoding, "S16LE") != 0) return 7;
    GstBuffer *buffer = gst_sample_get_buffer(sample);
    GstMapInfo mapped;
    if (!buffer || !gst_buffer_map(buffer, &mapped, GST_MAP_READ)) return 8;
    if (mapped.size != 8 || channels != 1) return 9;
    int16_t values[4];
    for (int i = 0; i < 4; ++i) values[i] =
        (int16_t) ((uint16_t) mapped.data[2*i] | ((uint16_t) mapped.data[2*i+1] << 8));
    printf("{\"sample_rate\":%d,\"channels\":%d,\"frames\":4,\"samples\":[%d,%d,%d,%d]}\n",
           rate, channels, values[0], values[1], values[2], values[3]);
    gst_buffer_unmap(buffer, &mapped);
    gst_sample_unref(sample);
    gst_element_set_state(pipeline, GST_STATE_NULL);
    gst_object_unref(source);
    gst_object_unref(sink);
    gst_object_unref(pipeline);
    return 0;
}
