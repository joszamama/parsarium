#define _GNU_SOURCE
#include "harness.h"
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavutil/pixfmt.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parsarium_parse_pnm(const uint8_t *data, size_t size, struct parsarium_pnm_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  char path[] = "/tmp/parsarium-ffmpeg-XXXXXX.ppm";
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
  AVCodecContext *decoder = NULL;
  AVPacket *packet = NULL;
  AVFrame *frame = NULL;
  int ok = 0;
  do {
    if (avformat_find_stream_info(ctx, NULL) < 0) break;
    const AVCodec *codec = NULL;
    int index = av_find_best_stream(ctx, AVMEDIA_TYPE_VIDEO, -1, -1, &codec, 0);
    if (index < 0 || !codec || ctx->streams[index]->codecpar->codec_id != AV_CODEC_ID_PPM) break;
    decoder = avcodec_alloc_context3(codec);
    if (!decoder || avcodec_parameters_to_context(decoder, ctx->streams[index]->codecpar) < 0 ||
        avcodec_open2(decoder, codec, NULL) < 0) break;
    packet = av_packet_alloc(); frame = av_frame_alloc();
    if (!packet || !frame) break;
    while (av_read_frame(ctx, packet) >= 0) {
      if (packet->stream_index == index && avcodec_send_packet(decoder, packet) >= 0 &&
          avcodec_receive_frame(decoder, frame) >= 0 && frame->width >= 2 &&
          frame->height >= 1 && frame->format == AV_PIX_FMT_RGB24) {
        const unsigned char *pixels = frame->data[0];
        result->width = frame->width; result->height = frame->height;
        for (int c = 0; c < 3; ++c) {
          result->first[c] = pixels[c]; result->second[c] = pixels[c + 3];
        }
        ok = 1;
        av_packet_unref(packet);
        break;
      }
      av_packet_unref(packet);
    }
  } while (0);
  av_frame_free(&frame); av_packet_free(&packet);
  avcodec_free_context(&decoder); avformat_close_input(&ctx);
  return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_pnm_result result;
  (void)parsarium_parse_pnm(data, size, &result);
  return 0;
}
