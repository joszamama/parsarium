#include <libheif/heif.h>
#include <libheif/heif_sequences.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    heif_context *context = heif_context_alloc();
    if (!context) return 1;
    heif_error error = heif_context_read_from_file(context, argv[1], NULL);
    if (error.code != heif_error_Ok) { heif_context_free(context); return 1; }

    int track_count = heif_context_number_of_sequence_tracks(context);
    if (track_count < 1 || track_count > 16) { heif_context_free(context); return 1; }
    uint32_t ids[16];
    heif_context_get_track_ids(context, ids);
    int video_tracks = 0;
    uint16_t width = 0, height = 0;
    for (int i = 0; i < track_count; i++) {
        heif_track *track = heif_context_get_track(context, ids[i]);
        if (!track) { heif_context_free(context); return 1; }
        if (heif_track_get_track_handler_type(track) == heif_track_type_video) {
            video_tracks++;
            error = heif_track_get_image_resolution(track, &width, &height);
            if (error.code != heif_error_Ok) { heif_track_release(track); heif_context_free(context); return 1; }
        }
        heif_track_release(track);
    }
    printf("{\"sequence_tracks\":%d,\"video_tracks\":%d,\"width\":%u,\"height\":%u}\n",
           track_count, video_tracks, width, height);
    heif_context_free(context);
    return 0;
}
