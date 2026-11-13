#include <gst/pbutils/pbutils.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  gst_init(NULL, NULL);
  gchar *path = g_canonicalize_filename(argv[1], NULL);
  gchar *uri = gst_filename_to_uri(path, NULL);
  g_free(path);
  if (!uri) return 1;
  GstDiscoverer *discoverer = gst_discoverer_new(5 * GST_SECOND, NULL);
  if (!discoverer) return 1;
  GstDiscovererInfo *info = gst_discoverer_discover_uri(discoverer, uri, NULL);
  if (!info || gst_discoverer_info_get_result(info) != GST_DISCOVERER_OK) return 1;
  const GstTagList *tags = gst_discoverer_info_get_tags(info);
  gchar *title = NULL;
  if (!tags || !gst_tag_list_get_string(tags, GST_TAG_TITLE, &title)) return 1;
  GList *video = gst_discoverer_info_get_video_streams(info);
  GList *audio = gst_discoverer_info_get_audio_streams(info);
  if (!video || video->next || !audio || audio->next) return 1;
  GstDiscovererVideoInfo *stream = GST_DISCOVERER_VIDEO_INFO(video->data);
  printf("{\"title\":\"%s\",\"video_tracks\":1,\"audio_tracks\":1,\"width\":%u,\"height\":%u}\n",
         title, gst_discoverer_video_info_get_width(stream),
         gst_discoverer_video_info_get_height(stream));
  g_free(title);
  gst_discoverer_stream_info_list_free(video);
  gst_discoverer_stream_info_list_free(audio);
  gst_discoverer_info_unref(info);
  g_object_unref(discoverer);
  g_free(uri);
  return 0;
}
