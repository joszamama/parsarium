#ifdef __cplusplus
extern "C" {
#endif
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavutil/pixfmt.h>
#ifdef __cplusplus
}
#endif
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    AVFormatContext *container = NULL;
    if (avformat_open_input(&container, argv[1], NULL, NULL) < 0) return 1;
    if (avformat_find_stream_info(container, NULL) < 0) return 1;
    const AVCodec *codec = NULL;
    int index = av_find_best_stream(container, AVMEDIA_TYPE_VIDEO, -1, -1, &codec, 0);
    if (index < 0 || !codec || container->streams[index]->codecpar->codec_id != AV_CODEC_ID_PPM) return 1;
    AVCodecContext *decoder = avcodec_alloc_context3(codec);
    if (!decoder || avcodec_parameters_to_context(decoder, container->streams[index]->codecpar) < 0 ||
        avcodec_open2(decoder, codec, NULL) < 0) return 1;
    AVPacket *packet = av_packet_alloc();
    AVFrame *frame = av_frame_alloc();
    if (!packet || !frame) return 1;
    int found = 0;
    while (av_read_frame(container, packet) >= 0) {
        if (packet->stream_index == index && avcodec_send_packet(decoder, packet) >= 0 &&
            avcodec_receive_frame(decoder, frame) >= 0) {
            found = 1;
            av_packet_unref(packet);
            break;
        }
        av_packet_unref(packet);
    }
    if (!found || frame->width != 2 || frame->height != 1 || frame->format != AV_PIX_FMT_RGB24) return 1;
    const unsigned char *pixels = frame->data[0];
    printf("{\"width\":%d,\"height\":%d,\"codec\":\"ppm\",\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
           frame->width, frame->height, pixels[0], pixels[1], pixels[2],
           pixels[3], pixels[4], pixels[5]);
    av_frame_free(&frame);
    av_packet_free(&packet);
    avcodec_free_context(&decoder);
    avformat_close_input(&container);
    return 0;
}
