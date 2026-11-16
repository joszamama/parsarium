#include "harness.h"
#include <gst/pbutils/pbutils.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parsarium_parse(const uint8_t *data, size_t size, struct parsarium_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.mp4";
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
        if (tags && gst_tag_list_get_string(tags, GST_TAG_TITLE, &title) &&
            strlen(title) < sizeof(result->title)) {
            memcpy(result->title, title, strlen(title) + 1);
            GList *video = gst_discoverer_info_get_video_streams(info);
            GList *audio = gst_discoverer_info_get_audio_streams(info);
            if (video && !video->next && audio && !audio->next) {
                GstDiscovererVideoInfo *stream = GST_DISCOVERER_VIDEO_INFO(video->data);
                result->width = gst_discoverer_video_info_get_width(stream);
                result->height = gst_discoverer_video_info_get_height(stream);
                result->video_tracks = 1;
                result->audio_tracks = 1;
                ok = result->width > 0 && result->height > 0;
            }
            gst_discoverer_stream_info_list_free(video);
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
