#include <stdio.h>
#include <xine.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    xine_t *engine = xine_new();
    if (!engine) return 2;
    xine_init(engine);
    xine_audio_port_t *audio = xine_open_audio_driver(engine, "none", NULL);
    xine_video_port_t *video = xine_open_video_driver(engine, "none", XINE_VISUAL_TYPE_NONE, NULL);
    if (!audio || !video) return 2;
    xine_stream_t *stream = xine_stream_new(engine, audio, video);
    if (!stream || !xine_open(stream, argv[1])) return 2;
    printf("{\"has_video\":%u,\"has_audio\":%u,\"width\":%u,\"height\":%u}\n",
           xine_get_stream_info(stream, XINE_STREAM_INFO_HAS_VIDEO),
           xine_get_stream_info(stream, XINE_STREAM_INFO_HAS_AUDIO),
           xine_get_stream_info(stream, XINE_STREAM_INFO_VIDEO_WIDTH),
           xine_get_stream_info(stream, XINE_STREAM_INFO_VIDEO_HEIGHT));
    xine_dispose(stream);
    xine_close_audio_driver(engine, audio);
    xine_close_video_driver(engine, video);
    xine_exit(engine);
    return 0;
}
