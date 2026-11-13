#include <libavformat/avformat.h>
#include <libavutil/dict.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    av_register_all();
    AVFormatContext *context = NULL;
    if (avformat_open_input(&context, argv[1], NULL, NULL) < 0) return 2;
    if (avformat_find_stream_info(context, NULL) < 0) return 2;
    AVDictionaryEntry *brand = av_dict_get(context->metadata, "major_brand", NULL, 0);
    unsigned video = 0, audio = 0, width = 0, height = 0;
    for (unsigned i = 0; i < context->nb_streams; ++i) {
        AVCodecParameters *codec = context->streams[i]->codecpar;
        if (codec->codec_type == AVMEDIA_TYPE_VIDEO) {
            ++video;
            width = codec->width;
            height = codec->height;
        } else if (codec->codec_type == AVMEDIA_TYPE_AUDIO) {
            ++audio;
        }
    }
    printf("{\"brand\":\"%s\",\"tracks\":%u,\"video\":%u,\"audio\":%u,\"width\":%u,\"height\":%u}\n",
           brand ? brand->value : "", context->nb_streams, video, audio, width, height);
    avformat_close_input(&context);
    return 0;
}
