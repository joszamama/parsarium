#ifdef __cplusplus
extern "C" {
#endif
#include <libavformat/avformat.h>
#include <libavutil/dict.h>
#ifdef __cplusplus
}
#endif
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  AVFormatContext *context = NULL;
  if (avformat_open_input(&context, argv[1], NULL, NULL) < 0) return 1;
  if (avformat_find_stream_info(context, NULL) < 0) return 1;
  AVDictionaryEntry *brand = av_dict_get(context->metadata, "major_brand", NULL, 0);
  AVDictionaryEntry *title = av_dict_get(context->metadata, "title", NULL, 0);
  unsigned video_tracks = 0, audio_tracks = 0, width = 0, height = 0;
  for (unsigned i = 0; i < context->nb_streams; i++) {
    AVCodecParameters *codec = context->streams[i]->codecpar;
    if (codec->codec_type == AVMEDIA_TYPE_VIDEO) {
      video_tracks++;
      width = codec->width;
      height = codec->height;
    } else if (codec->codec_type == AVMEDIA_TYPE_AUDIO) audio_tracks++;
  }
  if (!brand || !title || video_tracks != 1 || audio_tracks != 1) return 1;
  printf("{\"brand\":\"%s\",\"title\":\"%s\",\"video_tracks\":%u,\"audio_tracks\":%u,\"width\":%u,\"height\":%u}\n",
         brand->value, title->value, video_tracks, audio_tracks, width, height);
  avformat_close_input(&context);
  return 0;
}
