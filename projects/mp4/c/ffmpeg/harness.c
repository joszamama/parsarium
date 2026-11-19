#define _GNU_SOURCE
#include "harness.h"
#include <libavformat/avformat.h>
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
  if (avformat_find_stream_info(ctx, NULL) < 0) goto done;
  AVDictionaryEntry *brand = av_dict_get(ctx->metadata, "major_brand", NULL, 0);
  AVDictionaryEntry *title = av_dict_get(ctx->metadata, "title", NULL, 0);
  if ((brand && !(result->brand = strdup(brand->value))) ||
      (title && !(result->title = strdup(title->value)))) goto done;
  for (unsigned i = 0; i < ctx->nb_streams; ++i) {
    AVCodecParameters *codec = ctx->streams[i]->codecpar;
    if (codec->codec_type == AVMEDIA_TYPE_VIDEO) {
      if (!result->video_tracks++) { result->width = codec->width; result->height = codec->height; }
    } else if (codec->codec_type == AVMEDIA_TYPE_AUDIO) result->audio_tracks++;
  }
  ok = 1;
done:
  if (!ok) parsarium_free_mp4(result);
  avformat_close_input(&ctx);
  return ok;
}

void parsarium_free_mp4(struct parsarium_mp4_result *result) {
  free(result->brand); free(result->title);
  result->brand = result->title = NULL;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_mp4_result result;
  if (parsarium_parse_mp4(data, size, &result)) parsarium_free_mp4(&result);
  return 0;
}
