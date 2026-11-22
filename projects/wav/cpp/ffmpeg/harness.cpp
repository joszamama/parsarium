#define _GNU_SOURCE
#include "harness.h"
extern "C" {
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavutil/error.h>
#include <libavutil/samplefmt.h>
}
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/* One decoded sample as s16, for libraries that hand back their native
   sample format: unsigned integers are re-centred, wider integers keep their
   top 16 bits, floats are scaled by 32768, rounded and clamped. */
static int16_t parsarium_to_s16(const uint8_t *p, char kind, int bytes, int big_endian) {
    uint64_t raw = 0;
    for (int i = 0; i < bytes; i++)
        raw |= (uint64_t)p[big_endian ? i : bytes - 1 - i] << (8 * (bytes - 1 - i));
    if (kind == 'f') {
        double x;
        if (bytes == 4) { uint32_t bits = (uint32_t)raw; float f; memcpy(&f, &bits, 4); x = f; }
        else { double d; memcpy(&d, &raw, 8); x = d; }
        x = x * 32768.0;
        if (!(x > -32768.0)) return x != x ? 0 : -32768;
        if (x >= 32767.0) return 32767;
        return (int16_t)(x >= 0 ? x + 0.5 : x - 0.5); /* half away from zero */
    }
    if (kind == 'u') raw ^= (uint64_t)1 << (8 * bytes - 1);
    uint64_t top = bytes >= 2 ? raw >> (8 * bytes - 16) : raw << 8;
    return (int16_t)(uint16_t)(top & 0xFFFF);
}

static int failed(struct parsarium_wav_result *result, const char *call, int code) {
  char text[AV_ERROR_MAX_STRING_SIZE] = {0};
  av_strerror(code, text, sizeof(text));
  snprintf(result->error, sizeof(result->error), "%s: %s", call, text);
  return 0;
}

/* Append the first samples of a decoded frame, in interleaved order, as s16. */
static void take_samples(const AVFrame *frame, struct parsarium_wav_result *result) {
  enum AVSampleFormat format = (enum AVSampleFormat)frame->format;
  int channels = frame->ch_layout.nb_channels;
  int bytes = av_get_bytes_per_sample(format);
  int planar = av_sample_fmt_is_planar(format);
  enum AVSampleFormat packed = av_get_packed_sample_fmt(format);
  char kind = packed == AV_SAMPLE_FMT_U8 ? 'u' :
              packed == AV_SAMPLE_FMT_FLT || packed == AV_SAMPLE_FMT_DBL ? 'f' : 's';
  if (channels <= 0 || bytes <= 0) return;
  for (int index = 0; result->sample_count < 4 && index < frame->nb_samples * channels; index++) {
    int sample = index / channels, channel = index % channels;
    const uint8_t *p = planar ? frame->extended_data[channel] + (size_t)sample * bytes
                              : frame->extended_data[0] + ((size_t)sample * channels + channel) * bytes;
    result->samples[result->sample_count++] = parsarium_to_s16(p, kind, bytes, 0);
  }
}

int parsarium_parse_wav(const uint8_t *data, size_t size, struct parsarium_wav_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  char path[] = "/tmp/parsarium-ffmpeg-XXXXXX.wav";
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
  int code = avformat_open_input(&ctx, path, NULL, NULL);
  unlink(path);
  if (code < 0) return failed(result, "avformat_open_input", code);
  AVCodecContext *decoder = NULL;
  AVPacket *packet = NULL;
  AVFrame *frame = NULL;
  int ok = 0;
  do {
    if ((code = avformat_find_stream_info(ctx, NULL)) < 0) { failed(result, "avformat_find_stream_info", code); break; }
    const AVCodec *codec = NULL;
    int index = av_find_best_stream(ctx, AVMEDIA_TYPE_AUDIO, -1, -1, &codec, 0);
    if (index < 0) { failed(result, "av_find_best_stream", index); break; }
    AVStream *stream = ctx->streams[index];
    decoder = avcodec_alloc_context3(codec);
    if (!decoder) break;
    if ((code = avcodec_parameters_to_context(decoder, stream->codecpar)) < 0) { failed(result, "avcodec_parameters_to_context", code); break; }
    if ((code = avcodec_open2(decoder, codec, NULL)) < 0) { failed(result, "avcodec_open2", code); break; }
    packet = av_packet_alloc(); frame = av_frame_alloc();
    if (!packet || !frame) break;
    result->sample_rate = (unsigned)decoder->sample_rate;
    result->channels = (unsigned)decoder->ch_layout.nb_channels;
    AVRational sample_time = {1, decoder->sample_rate};
    result->frames = stream->duration == AV_NOPTS_VALUE || decoder->sample_rate <= 0 ? 0 :
      (unsigned long long)av_rescale_q(stream->duration, stream->time_base, sample_time);
    /* Decode until the first four samples are in, or the stream ends. */
    int error = 0, eof = 0;
    while (!error && result->sample_count < 4) {
      if (!eof) {
        code = av_read_frame(ctx, packet);
        if (code < 0) { eof = 1; code = avcodec_send_packet(decoder, NULL); }
        else if (packet->stream_index != index) { av_packet_unref(packet); continue; }
        else { code = avcodec_send_packet(decoder, packet); av_packet_unref(packet); }
        if (code < 0 && code != AVERROR_EOF) { failed(result, "avcodec_send_packet", code); error = 1; break; }
      }
      while (result->sample_count < 4 && (code = avcodec_receive_frame(decoder, frame)) >= 0) {
        take_samples(frame, result);
        av_frame_unref(frame);
      }
      if (code == AVERROR_EOF) break;
      if (code < 0 && code != AVERROR(EAGAIN)) { failed(result, "avcodec_receive_frame", code); error = 1; }
      else if (eof && code == AVERROR(EAGAIN)) break;
    }
    ok = !error;
  } while (0);
  av_frame_free(&frame); av_packet_free(&packet);
  avcodec_free_context(&decoder); avformat_close_input(&ctx);
  return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_wav_result result;
  (void)parsarium_parse_wav(data, size, &result);
  return 0;
}
