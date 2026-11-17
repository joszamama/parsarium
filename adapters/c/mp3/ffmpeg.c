#include <libavformat/avformat.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  AVFormatContext *format = NULL;
  if (avformat_open_input(&format, argv[1], NULL, NULL) < 0) return 1;
  if (avformat_find_stream_info(format, NULL) < 0) return 1;
  const AVDictionaryEntry *title = av_dict_get(format->metadata, "title", NULL, 0);
  int mp3_streams = 0;
  for (unsigned int i = 0; i < format->nb_streams; ++i)
    if (format->streams[i]->codecpar->codec_id == AV_CODEC_ID_MP3) ++mp3_streams;
  if (!title || mp3_streams == 0) return 1;
  printf("{\"title\":\"%s\",\"mp3_streams\":%d}\n", title->value, mp3_streams);
  avformat_close_input(&format);
  return 0;
}
