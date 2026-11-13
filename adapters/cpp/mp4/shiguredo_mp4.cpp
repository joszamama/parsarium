#include "mp4.h"
#include <stdint.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 1;
    struct Mp4FileDemuxer *demuxer = mp4_file_demuxer_new();
    if (!demuxer) { fclose(file); return 1; }

    uint8_t bytes[65536];
    for (;;) {
        uint64_t position = 0;
        int32_t size = 0;
        if (mp4_file_demuxer_get_required_input(demuxer, &position, &size) != MP4_ERROR_OK)
            return 1;
        if (size == 0) break;
        if (fseek(file, (long)position, SEEK_SET)) return 1;
        size_t requested;
        if (size < 0) {
            if (fseek(file, 0, SEEK_END)) return 1;
            long end = ftell(file);
            requested = (size_t)(end - (long)position);
            if (fseek(file, (long)position, SEEK_SET)) return 1;
        } else {
            requested = (size_t)size;
        }
        if (requested > sizeof(bytes)) return 1;
        size_t got = fread(bytes, 1, requested, file);
        if (mp4_file_demuxer_handle_input(demuxer, position, bytes, (uint32_t)got) != MP4_ERROR_OK)
            return 1;
    }

    const struct Mp4DemuxTrackInfo *tracks = NULL;
    uint32_t track_count = 0;
    if (mp4_file_demuxer_get_tracks(demuxer, &tracks, &track_count) != MP4_ERROR_OK)
        return 1;
    unsigned video = 0, audio = 0;
    unsigned long long video_duration_ms = 0;
    for (uint32_t i = 0; i < track_count; i++) {
        if (tracks[i].kind == MP4_TRACK_KIND_VIDEO) {
            video++;
            if (tracks[i].timescale)
                video_duration_ms = tracks[i].duration * 1000 / tracks[i].timescale;
        } else if (tracks[i].kind == MP4_TRACK_KIND_AUDIO) {
            audio++;
        }
    }
    printf("{\"tracks\":%u,\"video_tracks\":%u,\"audio_tracks\":%u,\"video_duration_ms\":%llu}\n",
           track_count, video, audio, video_duration_ms);
    mp4_file_demuxer_free(demuxer);
    fclose(file);
    return 0;
}
