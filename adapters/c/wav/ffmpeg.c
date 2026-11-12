#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavutil/samplefmt.h>
#include <stdint.h>
#include <string.h>

#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    AVFormatContext *container = NULL;
    if (avformat_open_input(&container, argv[1], NULL, NULL) < 0) return 3;
    if (avformat_find_stream_info(container, NULL) < 0 ||
        !container->iformat || strcmp(container->iformat->name, "wav") != 0) return 4;
    const AVCodec *codec = NULL;
    int index = av_find_best_stream(container, AVMEDIA_TYPE_AUDIO, -1, -1, &codec, 0);
    if (index < 0 || !codec) return 5;
    AVStream *stream = container->streams[index];
    AVCodecContext *decoder = avcodec_alloc_context3(codec);
    if (!decoder || avcodec_parameters_to_context(decoder, stream->codecpar) < 0 ||
        avcodec_open2(decoder, codec, NULL) < 0) return 6;
    AVPacket *packet = av_packet_alloc();
    AVFrame *frame = av_frame_alloc();
    if (!packet || !frame) return 7;
    int16_t samples[4] = {0};
    int found = 0;
    while (av_read_frame(container, packet) >= 0) {
        if (packet->stream_index == index && avcodec_send_packet(decoder, packet) >= 0 &&
            avcodec_receive_frame(decoder, frame) >= 0 &&
            frame->format == AV_SAMPLE_FMT_S16 && frame->nb_samples >= 4 &&
            frame->ch_layout.nb_channels == 1) {
            memcpy(samples, frame->data[0], sizeof(samples));
            found = 1;
            av_packet_unref(packet);
            break;
        }
        av_packet_unref(packet);
    }
    if (!found || stream->duration == AV_NOPTS_VALUE) return 8;
    uint64_t frames = (uint64_t)av_rescale_q(stream->duration, stream->time_base,
                                              (AVRational){1, decoder->sample_rate});
    wav_report((unsigned int)decoder->sample_rate,
               (unsigned int)decoder->ch_layout.nb_channels, frames, samples);
    av_frame_free(&frame);
    av_packet_free(&packet);
    avcodec_free_context(&decoder);
    avformat_close_input(&container);
    return 0;
}
