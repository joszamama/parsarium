#include <gst/app/gstappsink.h>
#include <gst/gst.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    gst_init(&argc, &argv);
    GError *error = NULL;
    GstElement *pipeline = gst_parse_launch(
        "filesrc name=source ! pnmdec ! appsink name=sink sync=false", &error);
    if (!pipeline || error) return 1;
    GstElement *source = gst_bin_get_by_name(GST_BIN(pipeline), "source");
    GstElement *sink = gst_bin_get_by_name(GST_BIN(pipeline), "sink");
    if (!source || !sink) return 1;
    g_object_set(source, "location", argv[1], NULL);
    if (gst_element_set_state(pipeline, GST_STATE_PLAYING) == GST_STATE_CHANGE_FAILURE) return 1;
    GstSample *sample = gst_app_sink_try_pull_sample(GST_APP_SINK(sink), 5 * GST_SECOND);
    if (!sample) return 1;
    GstCaps *caps = gst_sample_get_caps(sample);
    const GstStructure *format = caps ? gst_caps_get_structure(caps, 0) : NULL;
    int width = 0, height = 0;
    const char *encoding = format ? gst_structure_get_string(format, "format") : NULL;
    if (!format || !gst_structure_get_int(format, "width", &width) ||
        !gst_structure_get_int(format, "height", &height) ||
        !encoding || strcmp(encoding, "RGB") != 0) return 1;
    GstBuffer *buffer = gst_sample_get_buffer(sample);
    GstMapInfo mapped;
    if (!buffer || !gst_buffer_map(buffer, &mapped, GST_MAP_READ)) return 1;
    if (width != 2 || height != 1 || mapped.size < 6) return 1;
    printf("{\"width\":%d,\"height\":%d,\"format\":\"RGB\",\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
           width, height, mapped.data[0], mapped.data[1], mapped.data[2],
           mapped.data[3], mapped.data[4], mapped.data[5]);
    gst_buffer_unmap(buffer, &mapped);
    gst_sample_unref(sample);
    gst_element_set_state(pipeline, GST_STATE_NULL);
    gst_object_unref(source);
    gst_object_unref(sink);
    gst_object_unref(pipeline);
    return 0;
}
