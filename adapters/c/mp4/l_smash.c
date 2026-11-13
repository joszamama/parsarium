#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

#include "lsmash.h"

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "expected one local MP4 path\n");
        return 2;
    }
    lsmash_root_t *root = lsmash_create_root();
    if (!root) return 2;
    lsmash_file_parameters_t file_param = {0};
    if (lsmash_open_file(argv[1], 1, &file_param) < 0) return 2;
    lsmash_file_t *file = lsmash_set_file(root, &file_param);
    if (!file || lsmash_read_file(file, &file_param) < 0) return 2;

    lsmash_movie_parameters_t movie;
    lsmash_initialize_movie_parameters(&movie);
    if (lsmash_get_movie_parameters(root, &movie) < 0) return 2;
    unsigned video = 0;
    unsigned audio = 0;
    unsigned width = 0;
    unsigned height = 0;
    for (uint32_t number = 1; number <= movie.number_of_tracks; ++number) {
        uint32_t id = lsmash_get_track_ID(root, number);
        if (!id) return 2;
        lsmash_media_parameters_t media;
        lsmash_initialize_media_parameters(&media);
        if (lsmash_get_media_parameters(root, id, &media) < 0) return 2;
        if (media.handler_type == ISOM_MEDIA_HANDLER_TYPE_VIDEO_TRACK) {
            lsmash_track_parameters_t track;
            lsmash_initialize_track_parameters(&track);
            if (lsmash_get_track_parameters(root, id, &track) < 0) return 2;
            ++video;
            width = track.display_width >> 16;
            height = track.display_height >> 16;
        } else if (media.handler_type == ISOM_MEDIA_HANDLER_TYPE_AUDIO_TRACK) {
            ++audio;
        }
    }
    uint64_t duration_ms = movie.timescale ? movie.duration * 1000 / movie.timescale : 0;
    printf("{\"tracks\":%u,\"video\":%u,\"audio\":%u,\"width\":%u,\"height\":%u,\"duration_ms\":%" PRIu64 "}\n",
           movie.number_of_tracks, video, audio, width, height, duration_ms);
    lsmash_close_file(&file_param);
    lsmash_destroy_root(root);
    return 0;
}
