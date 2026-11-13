#include "mov-reader.h"
#include "mov-file-buffer.h"
#include <stdio.h>

static int video_tracks, audio_tracks, width, height;

static void onvideo(void *context, uint32_t track, uint8_t codec, int w, int h,
                    const void *extra, size_t extra_size) {
    (void)context; (void)track; (void)codec; (void)extra; (void)extra_size;
    video_tracks++;
    width = w;
    height = h;
}

static void onaudio(void *context, uint32_t track, uint8_t codec, int channels,
                    int sample_bits, int sample_rate, const void *extra, size_t extra_size) {
    (void)context; (void)track; (void)codec; (void)channels;
    (void)sample_bits; (void)sample_rate; (void)extra; (void)extra_size;
    audio_tracks++;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 1;
    mov_reader_t *reader = mov_reader_create(mov_file_buffer(), file);
    if (!reader) { fclose(file); return 1; }
    struct mov_reader_trackinfo_t callbacks = {onvideo, onaudio, NULL};
    if (mov_reader_getinfo(reader, &callbacks, NULL) != 0) {
        mov_reader_destroy(reader);
        fclose(file);
        return 1;
    }
    printf("{\"video_tracks\":%d,\"audio_tracks\":%d,\"width\":%d,\"height\":%d,\"duration_ms\":%llu}\n",
           video_tracks, audio_tracks, width, height,
           (unsigned long long)mov_reader_getduration(reader));
    mov_reader_destroy(reader);
    fclose(file);
    return 0;
}
