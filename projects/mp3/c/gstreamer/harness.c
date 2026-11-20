#include "harness.h"
#include <gst/pbutils/pbutils.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parsarium_parse(const uint8_t *data, size_t size, struct parsarium_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.mp3";
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
    gchar *uri = gst_filename_to_uri(path, NULL);
    if (!uri) { unlink(path); return 0; }
    GstDiscoverer *discoverer = gst_discoverer_new(5 * GST_SECOND, NULL);
    if (!discoverer) { g_free(uri); unlink(path); return 0; }
    GstDiscovererInfo *info = gst_discoverer_discover_uri(discoverer, uri, NULL);
    int ok = 0;
    if (info && gst_discoverer_info_get_result(info) == GST_DISCOVERER_OK) {
        const GstTagList *tags = gst_discoverer_info_get_tags(info);
        gchar *title = NULL;
        result->has_title = tags && gst_tag_list_get_string(tags, GST_TAG_TITLE, &title);
        if (!result->has_title || strlen(title) < sizeof(result->title)) {
            if (result->has_title) memcpy(result->title, title, strlen(title) + 1);
                    GList *audio = gst_discoverer_info_get_audio_streams(info);
            if (audio && !audio->next) {
                GstDiscovererAudioInfo *stream = GST_DISCOVERER_AUDIO_INFO(audio->data);
                result->sample_rate = gst_discoverer_audio_info_get_sample_rate(stream);
                result->channels = gst_discoverer_audio_info_get_channels(stream);
                result->audio_streams = 1;
                ok = result->sample_rate > 0 && result->channels > 0;
            }
                    gst_discoverer_stream_info_list_free(audio);
        }
        g_free(title);
    }
    if (info) gst_discoverer_info_unref(info);
    g_object_unref(discoverer);
    g_free(uri);
    unlink(path);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_result result;
    (void)parsarium_parse(data, size, &result);
    return 0;
}
