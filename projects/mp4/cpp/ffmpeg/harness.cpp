#define _GNU_SOURCE
#include "harness.h"
extern "C" {
#include <libavformat/avformat.h>
}
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parsarium_parse_mp4(const uint8_t *data, size_t size, struct parsarium_mp4_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  char path[] = "/tmp/parsarium-ffmpeg-XXXXXX.mp4";
  int fd = mkstemps(path, 4);
  if (fd < 0) return 0;
  size_t written = 0;
  while (written < size) {
    ssize_t n = write(fd, data + written, size - written);
    if (n <= 0) { close(fd); unlink(path); return 0; }
    written += (size_t)n;
  }
  close(fd);
  AVFormatContext *ctx = NULL;
  int opened = avformat_open_input(&ctx, path, NULL, NULL);
  unlink(path);
  if (opened < 0) return 0;
  int ok = 0;
  AVDictionaryEntry *brand = NULL, *title = NULL;
  if (avformat_find_stream_info(ctx, NULL) < 0) goto done;
  brand = av_dict_get(ctx->metadata, "major_brand", NULL, 0);
  title = av_dict_get(ctx->metadata, "title", NULL, 0);
  if (!brand || !title || strlen(brand->value) >= sizeof(result->brand) ||
      strlen(title->value) >= sizeof(result->title)) goto done;
  strcpy(result->brand, brand->value); strcpy(result->title, title->value);
  for (unsigned i = 0; i < ctx->nb_streams; ++i) {
    AVCodecParameters *codec = ctx->streams[i]->codecpar;
    if (codec->codec_type == AVMEDIA_TYPE_VIDEO) {
      result->video_tracks++;
      result->width = codec->width; result->height = codec->height;
    } else if (codec->codec_type == AVMEDIA_TYPE_AUDIO) result->audio_tracks++;
  }
  ok = result->video_tracks > 0 && result->audio_tracks > 0;
done:
  avformat_close_input(&ctx);
  return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_mp4_result result;
  (void)parsarium_parse_mp4(data, size, &result);
  return 0;
}
